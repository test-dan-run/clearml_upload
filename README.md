# ClearML Common Use Cases

This repository has only been tested on linux-based systems. (Including WSL)

## Requirements
Please make sure that you have clearml and boto3 installed in your local/virtual environment.
To create a virtual environment for clearml, run the following lines of code in your bash terminal.

```bash
# creates a python virtual env in your home folder
python3 -m venv ~/clearml
source ~/clearml/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install clearml boto3
```

You will need boto3 as clearml will attempt to ping the S3 storage server (if you have s3://... in your output_uri) before executing tasks.

## ClearML Config
You will also need to ensure your credentials in your config are written correctly.
Open up your `~/clearml.conf`, navigate to the s3 configs, and update as follows.

```
sdk {
    ...
    ...
    aws {
        s3 {
            region: ""
            key: ""
            secret: ""

            credentials: [
                host: xx.yy.zz:80
                key: abc
                secret: @#$
                multipart: false
                secure: false
            ]
        }
    }
}
```
