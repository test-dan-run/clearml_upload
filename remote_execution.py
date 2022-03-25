from clearml import Task

#### PARAMS ####

PROJECT_NAME = 'example_projects'
TASK_NAME = 'example_task'

# s3://<server url>:<port>/<bucket>/...
OUTPUT_URI = 's3://min.io:80/clearml-data/default'
QUEUE_NAME = 'sample-gpu-queue'

################

task = Task.init(
    project_name = PROJECT_NAME,
    task_name = TASK_NAME,
    output_uri = OUTPUT_URI
)

task.set_base_docker('docker.io/sample/nvidia_gpu_image:v1.0.0-base --env TRAINS_AGENT_GIT_USER=testuser --env TRAINS_AGENT_GIT_PASS=123 --env GIT_SSL_NO_VERIFY=true')
task.execute_remotely(queue_name=QUEUE_NAME, clone=False, exit_process=True)

#### TRAINING CODE ####

# insert your training code here as per normal

# import torch
# ...
# ...
