import os
from googleapiclient.discovery import build

def _dataflow_job_start(data, context):
    # read from gcs
    PROJECTID = os.environ['PROJECTID']
    SOURCE_BUCKET = os.environ['SOURCE_BUCKET']
    DATA_BUCKET = data['bucket']
    file_path = data['name']
    if not file_path.startswith('file_prefix/'):
      return 0
    job = 'replace_text_' + '_'.join(file_path.split('/'))
    template = f"gs://{SOURCE_BUCKET}/template/replace_text"
    parameters = {
         'input': f"gs://{DATA_BUCKET}/{file_path}",
         'output': f"gs://{DATA_BUCKET}/output/{file_path}"
    }
    environment = {
        'tempLocation': f"gs://{SOURCE_BUCKET}/temp/{file_path}"
    }

    service  = build(
        "dataflow","v1b3",
        cache_discovery=False)
    request = service.projects().locations().templates().launch(
        projectId=PROJECTID,
        location='asia-northeast1',
        gcsPath=template,
        body={
            'jobName': job,
            'parameters': parameters,
            'environment': environment
        }
    )
    response = request.execute()
    print(response)
    return response
