import os
from clearml import Task, Dataset
from typing import List
import json

#### PARAMS ####

PARENT_DATASET_IDS = ['709a1943cd0c4db18ec32cb17d978541', '01288ee80cf642d685496b89b07f819a','2d31814fec934b379d15d014d7d22717']
ARTIFACT_NAME = 'train_manifest.json'

DATASET_PROJECT = 'datasets/combined_asr/ar/wav_16k'
DATASET_NAME = 'train'

# s3://<server url>:<port>/<bucket>/...
OUTPUT_URI = 's3://experiment-logging/storage'

################

def combine_datasets(
    dataset_project: str, 
    dataset_name: str,
    artifact_name: str,
    parent_ids: List[str] = None,
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

    manifest_items = []
    for parent_id in parent_ids:
        parent_task = Task.get_task(task_id=parent_id)
        manifest_path = parent_task.artifacts[artifact_name].get_local_copy()
        with open(manifest_path, mode='r', encoding='utf-8') as fr:
            lines = fr.readlines()
            for line in lines:
                manifest_items.append(json.loads(line.strip('\r\n')))

    with open(artifact_name, mode='w', encoding='utf-8') as fw:
        for item in manifest_items:
            fw.write(json.dumps(item)+'\n')

    # intialize dataset task as current task
    dataset = Dataset.create(
        dataset_project = dataset_project,
        dataset_name = dataset_name,
        parent_datasets = parent_ids,
        use_current_task = True
    )

    # add all files in the local directory
    dataset.add_files(artifact_name)
    # upload dataset to remote storage
    dataset.upload(
        output_url=output_uri, 
        verbose=True
    )

    task.upload_artifact(
        name = artifact_name, 
        artifact_object = artifact_name
    )
    
    # finalize the dataset
    dataset.finalize()

    # end the task
    task.close()

if __name__ == '__main__':

    combine_datasets(
        dataset_project = DATASET_PROJECT,
        dataset_name = DATASET_NAME,
        artifact_name = ARTIFACT_NAME,
        parent_ids = PARENT_DATASET_IDS,
        output_uri = OUTPUT_URI
    )