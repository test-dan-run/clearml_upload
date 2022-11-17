import os
from clearml import Task, Dataset, Logger
from typing import List, Optional, Any
import json
import pandas as pd
import plotly.express as px

#### PARAMS ####

PARENT_DATASET_IDS = ['971b2303bcf74aee89889d7427e04592', '0fb20f414cca4ab1b9ee15db28d37a0e',]
ARTIFACT_NAME = 'test_manifest.json'

DATASET_PROJECT = 'audio/speech_recognition'
DATASET_NAME = 'cv-corpus-11.0-yue-wav16k'

# s3://<server url>:<port>/<bucket>/...
OUTPUT_URI = None

def commonvoice_stats(manifest_path: str, logger: Logger) -> None:
    df = pd.read_json(manifest_path, lines=True)
    df['num_chars'] = df['text'].apply(lambda x: len(x))
    df['num_words'] = df['text'].apply(lambda x: len(x.split(' ')))
    df = df.fillna(value='none')

    fig = px.histogram(df, x='age')
    logger.report_plotly(title='Entries by Age', series='Entries', figure=fig)

    fig = px.histogram(df, x='accent')
    logger.report_plotly(title='Entries by Accent', series='Entries', figure=fig)

    fig = px.histogram(df, x='gender')
    logger.report_plotly(title='Entries by Gender', series='Entries', figure=fig)

    fig = px.histogram(df, x='num_chars')
    logger.report_plotly(title='Entries by Number of Characters', series='Entries', figure=fig)

    fig = px.histogram(df, x='num_words')
    logger.report_plotly(title='Entries by Number of Words', series='Entries', figure=fig)

PLOT_FN = lambda logger: commonvoice_stats(ARTIFACT_NAME, logger)

################

def combine_datasets(
    dataset_project: str, 
    dataset_name: str,
    artifact_name: str,
    parent_ids: List[str] = None,
    output_uri: str = None,
    plot_fn: Optional[Any] = None
    ) -> None:
    '''
    artifact_paths: local files into easily accessible clearml files that can be used via the web UI or programatically
    parent_ids: ids of parent datasets if wish to extend from existing parent datasets
    '''

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
        use_current_task = False
    )

    # add all files in the local directory
    dataset.add_files(artifact_name)
    # upload dataset to remote storage
    dataset.upload(
        output_url=output_uri, 
        verbose=True
    )

    task = Task.get_task(dataset.id)
    task.upload_artifact(
        name = artifact_name, 
        artifact_object = artifact_name
    )
    
        # upload plots
    if plot_fn: 
        logger = task.get_logger()
        plot_fn(logger)

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
        output_uri = OUTPUT_URI,
        plot_fn = PLOT_FN
    )