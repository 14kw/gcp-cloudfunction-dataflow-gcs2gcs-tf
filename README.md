# gcp-cloudfunction-dataflow-gcs2gcs-tf

## create dataflow template

```
cd dataflow
python3 -m virtualenv .env
source .env/bin/activate
pip install apache-beam[gcp]

python replace_text.py \
--project=your-project-id \
--runner=DataflowRunner \
--staging_location=gs://your-source-bucket/staging \
--temp_location gs://your-source-bucket/temp \
--save_main_session \
--region asia-northeast1 \
--network your-vpc \
--subnetwork regions/asia-northeast1/subnetworks/your-subnet \
--template_location gs://your-source-bucket/template/replace_text
```

## deploy

```
cd cloudfunction
zip -r src.zip ./*
gsutil cp ./src.zip gs://your-source-bucket/run-replace-text-job-function/src.zip

export GOOGLE_APPLICATION_CREDENTIALS={{service account credentials path}}
terraform init
terraform plan
terraform apply
```

## note

[Cloud Function Crashes with message "finished with status 'crash'", Python 3\.7 runtime \[157063276\] \- Visible to Public \- Issue Tracker](https://issuetracker.google.com/issues/157063276)