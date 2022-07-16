import os
import json
from clearml import Task, Dataset
from typing import Dict, Any, Union, List

#### PARAMS ####

PARENT_DATASET_ID = '01288ee80cf642d685496b89b07f819a'
ARTIFACT_PATH = 'train_manifest.json'

DATASET_PROJECT = 'datasets/mediaspeech/ar/wav_16k'
DATASET_NAME = 'train_cleaned'

# s3://<server url>:<port>/<bucket>/...
OUTPUT_URI = 's3://experiment-logging/storage'

CLEAN_CONFIG = {
    'remove_punct': True,
    'remove_english': True,
    'remove_insuff_chars': True,
    'insuff_thres': 50
}

### HELPER FUNCTIONS ###
ENGLISH_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890'

def remove_punctuations_in_text(text: str) -> str:
    # remove punctuations
    text = ''.join(e for e in text if (e.isalnum() or e == ' '))
    # remove double spaces
    text = ''.join(text.split())
    return text

def remove_punctuations_in_item(item: Dict[str, Any]) -> Dict[str, Any]:
    item['text'] = remove_punctuations_in_text(item['text'])
    return item

def characters_in_text(text: str, characters:Union[List[str], str]) -> bool:
    return any([ch in characters for ch in text])

def extract_char_counts_in_items(items: List[Dict[str, Any]]) -> Dict[str, int]:
    
    char2count = {}
    for item in items:
        text = item['text']
        for ch in text:
            if ch not in char2count:
                char2count[ch] = 0
            char2count[ch] += 1
            
    return char2count

def clean_transcripts_in_manifest(
    artifact_path: str, output_path: str, 
    remove_punct: bool, remove_english: bool, 
    remove_insuff_chars: bool, insuff_thres: Union[int, float] = 0.01
    ) -> str:

    with open(artifact_path, mode='r', encoding='utf-8') as fr:
        lines = fr.readlines()
    items = [json.loads(line) for line in lines]

    if remove_punct:
        items = [remove_punctuations_in_item(item) for item in items]
    if remove_english:
        items = [item for item in items if not characters_in_text(item['text'], ENGLISH_CHARACTERS)]
    if remove_insuff_chars:
        char2count = extract_char_counts_in_items(items)
        min_count = insuff_thres if type(insuff_thres) is int else insuff_thres*len(items)
        char_to_remove = [k for k in char2count.keys() if char2count[k] < min_count]
        items = [item for item in items if not characters_in_text(item['text'], char_to_remove)]

    with open(output_path, mode='w', encoding='utf-8') as fw:
        for item in items:
            fw.write(json.dumps(item)+'\n')

    return output_path

################

def upload_dataset(
    parent_id: str,
    dataset_project: str, 
    dataset_name: str,
    artifact_name: str, 
    cfg: Dict[str, Any],
    output_uri: str = None
    ) -> None:
    '''
    artifact_paths: local files into easily accessible clearml files that can be used via the web UI or programatically
    parent_ids: ids of parent datasets if wish to extend from existing parent datasets
    '''

    # initialize empty task
    task = Task.init(
        project_name = dataset_project, 
        task_name = dataset_name, 
        output_uri=output_uri,
        task_type='data_processing'
        )

    # intialize dataset task as current task
    dataset = Dataset.create(
        dataset_project = dataset_project,
        dataset_name = dataset_name,
        parent_datasets = [parent_id,],
        use_current_task = True
    )

    dataset_task = Task.get_task(task_id=parent_id)
    artifact_path = dataset_task.artifacts[artifact_name].get_local_copy()
    manifest_path = clean_transcripts_in_manifest(artifact_path, output_path=artifact_name, **cfg)

    # add all files in the local directory
    dataset.add_files(manifest_path)
    # upload dataset to remote storage
    dataset.upload(
        output_url=output_uri, 
        verbose=True
    )

    task.upload_artifact(name=artifact_name, artifact_object=manifest_path)

    # finalize the dataset
    dataset.finalize()

    # end the task
    task.close()

if __name__ == '__main__':

    upload_dataset(
        parent_id = PARENT_DATASET_ID,
        dataset_project = DATASET_PROJECT,
        dataset_name = DATASET_NAME,
        artifact_name = ARTIFACT_PATH,
        cfg = CLEAN_CONFIG,
        output_uri = OUTPUT_URI
    )