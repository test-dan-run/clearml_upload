from clearml import Task

#### PARAMS ####

PROJECT_NAME = 'pretrained_models/nemo'
MODEL_NAME = 'stt_en_conformer_ctc_large_v1.10.0'

# s3://<server url>:<port>/<bucket>/...
OUTPUT_URI = 's3://experiment-logging/storage'
LOCAL_MODEL_PATH = '/mnt/c/Users/tjinghua/Downloads/stt_en_conformer_ctc_large.nemo'

################

def upload_model(
    project_name : str, 
    model_name: str, 
    local_model_path: str, 
    output_uri: str
    ) -> None:

    # initialize an empty task
    task = Task.init(
        project_name = project_name,
        task_name = model_name,
        output_uri = output_uri
    )

    # upload model as output model of the task
    task.update_output_model(
        model_path = local_model_path,
        name = model_name,
        model_name = model_name
    )

    # close the task
    task.close()


if __name__ == '__main__':

    upload_model(
        project_name = PROJECT_NAME,
        model_name = MODEL_NAME,
        local_model_path = LOCAL_MODEL_PATH,
        output_uri = OUTPUT_URI
    )