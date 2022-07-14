# ClearML-NeMo Required Structure

Directory structure
```
speech_dir
├── train
|   ├── train_data 
|   |   ├── train1.wav
|   |   ├── train2.wav
|   |   └── train3.wav
|   ├── train_manifest.json
|
├── dev
|   ├── dev_data 
|   |   ├── dev1.wav
|   |   ├── dev2.wav
|   |   └── dev3.wav
|   ├── dev_manifest.json
|
├── test
|   ├── test_data 
|   |  ├── test1.wav
|   |  ├── test2.wav
|   |  └── test3.wav
|   ├── test_manifest.json
|
```

Manifest structure
(test_manifest.json)
```
{"audio_filepath": "test_data/test1.wav", "text": "xxx", "duration": 4.32}
{"audio_filepath": "test_data/test2.wav", "text": "yyy", "duration": 4.33}
{"audio_filepath": "test_data/test3.wav", "text": "zzz", "duration": 4.34}
```

## Uploading to Clearml
Before uploading to ClearML, edit the parameters in `upload_dataset.py`
```
DATASET_PROJECT = 'datasets/jtube/id/wav_16k'
DATASET_NAME = 'train'
LOCAL_DATASET_DIR = '/mnt/d/datasets/jtube/id/wav_16k/train'
ARTIFACT_PATHS = ['/mnt/d/datasets/jtube/id/wav_16k/train/train_manifest.json',]

# s3://<server url>:<port>/<bucket>/...
OUTPUT_URI = 's3://experiment-logging/storage'
```
Then, upload to clearml via this command (Make sure you have clearml and boto3 pip installed)
```
python3 upload_dataset.py
```