# Upload Zipped Datasets

As intended by ClearML, you're supposed to upload a non-zipped folder, and ClearML
will zip and index the data within for you.

If your dataset is huge and is already zipped however, it's best not to unzip in your local environment.
Unless you wanna be stuck in the office looking at loading bars.

Instead, we will do it remotely! Why use your local memory when you can use cloud resources amirite.

The flow would be like this:

1. [Local Environment] Upload to S3 via StorageManager API
2. [Local Environment] Execute remote execution script
3. [Remote Environment] Download zipped file from S3 via StorageManager API
4. [Remote Environment] Unzip file via StorageManager API (3 and 4 will be executed simultaneously via the same method call)
5. [Remote Environment] Upload unzipped file as Dataset

## Steps

*NOTE*: Please test out with a small zipped dataset of the same file structure first.

1. Update `configs.py` with your filepath and project name
2. Run the following lines on your bash terminal.

```bash
source ~/clearml/bin/activate
# local upload to S3
python3 local_upload.py
# remote execution
python3 remote_upload.py
```