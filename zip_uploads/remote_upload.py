import os
from typing import List
from configs import UploadConfig
from clearml import StorageManager, Dataset, Task

cfg = UploadConfig()

# execute remote task
task = Task.init(
    project_name = cfg.project_name,
    task_name = cfg.task_name,
    output_uri = cfg.remote_uri
)

task.execute_remotely(queue_name=cfg.queue_name, clone=False, exit_process=True)

def list_files(startpath: str, max_files_per_folder: int = 4):
    # list files in a tree structure
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for idx, f in enumerate(files):
            if idx == max_files_per_folder:
                break
            print('{}{}'.format(subindent, f))

def download_storagemanager(remote_url: str, extract_from_archive: bool = True):
    # get copy of the zipped file from s3
    # extract from zip file set to true
    # returns the path

    path = StorageManager.get_local_copy(
        remote_url, 
        extract_from_archive=extract_from_archive
        )
    list_files(path)

    return path 

def upload_dataset(
    dataset_project: str, 
    dataset_name: str,
    local_dataset_dir: str,
    artifact_paths: List[str] = [], 
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

    # add artifacts
    for artifact_path in artifact_paths:
        task.upload_artifact(
            name = os.path.basename(artifact_path), 
            artifact_object = artifact_path
        )

    # intialize dataset task as current task
    dataset = Dataset.create(
        dataset_project = dataset_project,
        dataset_name = dataset_name,
        parent_datasets = parent_ids,
        use_current_task = True
    )

    # add all files in the local directory
    dataset.add_files(local_dataset_dir)
    
    # upload dataset to remote storage
    dataset.upload(
        output_url=output_uri, 
        verbose=True
    )

    # finalize the dataset
    dataset.finalize()

    # end the task
    task.close()

if __name__ == '__main__':

    path_to_dir = download_storagemanager(
        remote_url=os.path.join(cfg.temp_remote_uri, os.path.basename(cfg.local_path))
        )

    upload_dataset(
        dataset_project = cfg.dataset_project_name,
        dataset_name = cfg.dataset_name,
        local_dataset_dir = path_to_dir,
        artifact_paths = [],
        parent_ids = None,
        output_uri = cfg.remote_uri
    )