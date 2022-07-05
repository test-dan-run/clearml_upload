import os

class UploadConfig:
    def __init__(self):

        # for local upload to S3 via ClearML StorageManager
        self.temp_remote_uri = 's3://xx.yy.zz:80/clearml-data/temp_datasets'
        self.local_path = ''

        # for upload as actual ClearML Dataset
        self.remote_uri = 's3://xx.yy.zz:80/clearml-data/datasets'
        self.queue_name = 'sample-gpu-queue'
        self.base_docker_image = 'xxx'

        # change to your project name and how you wanna refer to the dataset
        # currently no best practice for dataset naming, I usually just put version name
        self.project_name = 'cute_project'
        self.dataset_name = 'version1_less_data'

        # no need change
        self.task_name = 'upload_zipped_dataset'
        self.dataset_project_name = os.path.join(self.project_name, 'datasets')
