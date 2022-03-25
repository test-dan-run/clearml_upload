from clearml import Dataset

#### PARAMS ####

DATASET_PROJECT = 'example_projects/sample_datasets'
DATASET_NAME = 'train_split'

DATASET_ID = 'asdkaqw89qj'

################

def download_via_project_name(dataset_project: str, dataset_name: str) -> str:
    '''
    if there are multiple datasets with the same dataset_project + dataset_name, the latest copy will be downloaded
    '''

    dataset = Dataset.get(dataset_project=dataset_project, dataset_name=dataset_name)
    dataset_path = dataset.get_local_copy()

    return dataset_path

def download_via_project_id(dataset_id: str) -> str:
    '''
    more secure since there is always only 1 unique id for each task
    '''

    dataset = Dataset.get(dataset_id=dataset_id)
    dataset_path = dataset.get_local_copy()

    return dataset_path