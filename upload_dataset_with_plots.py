import os
import pandas as pd
import plotly.express as px
from typing import List, Optional, Any
from clearml import Task, Dataset, Logger

#### PARAMS ####

DATASET_PROJECT = 'audio/speech_recognition'
DATASET_NAME = 'cv-corpus-10.0-zh-TW-test'
LOCAL_DATASET_DIR = '/mnt/d/datasets/cv-corpus-10.0-delta-2022-07-04/test'
ARTIFACT_PATHS = ['/mnt/d/datasets/cv-corpus-10.0-delta-2022-07-04/test/test_manifest.json',]

# # s3://<server url>:<port>/<bucket>/...
# OUTPUT_URI = 's3://experiment-logging/storage'
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


PLOT_FN = lambda logger: commonvoice_stats(ARTIFACT_PATHS[0], logger)

################

def upload_dataset_with_plots(
    dataset_project: str, 
    dataset_name: str,
    local_dataset_dir: str,
    artifact_paths: List[str] = [], 
    parent_ids: Optional[List[str]] = None,
    plot_fn: Optional[Any] = None,
    output_uri: str = None
    ) -> None:
    '''
    artifact_paths: local files into easily accessible clearml files that can be used via the web UI or programatically
    parent_ids: ids of parent datasets if wish to extend from existing parent datasets
    '''

    # intialize dataset task as current task
    dataset = Dataset.create(
        dataset_project = dataset_project,
        dataset_name = dataset_name,
        parent_datasets = parent_ids,
        use_current_task = False
    )

    # add all files in the local directory
    dataset.add_files(local_dataset_dir)
    

    # upload dataset to remote storage
    dataset.upload(
        output_url=output_uri, 
        verbose=True
    )

    # add artifacts
    task = Task.get_task(dataset.id)
    for artifact_path in artifact_paths:
        task.upload_artifact(
            name = os.path.basename(artifact_path), 
            artifact_object = artifact_path
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

    upload_dataset_with_plots(
        dataset_project = DATASET_PROJECT,
        dataset_name = DATASET_NAME,
        local_dataset_dir = LOCAL_DATASET_DIR,
        artifact_paths = ARTIFACT_PATHS,
        parent_ids = None,
        plot_fn = PLOT_FN,
        output_uri = OUTPUT_URI
    )