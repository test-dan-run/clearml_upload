import os
from configs import UploadConfig
from clearml import StorageManager

def upload_storagemanager(local_path: str, remote_uri: str) -> str:
    '''
    local_path: the local path to your desired file to upload
    remote_uri: the url to your remote storage (s3)
    '''
    assert os.path.exists(local_path), f'{local_path} does not exist!'

    upload_url = os.path.join(remote_uri, os.path.basename(local_path))
    
    return StorageManager.upload_file(local_path, upload_url)

if __name__ == '__main__':
    
    cfg = UploadConfig()
    upload_storagemanager(cfg.local_path, cfg.temp_remote_uri)