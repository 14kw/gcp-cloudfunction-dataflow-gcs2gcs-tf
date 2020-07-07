variable "project" {}
variable "region" {}
variable "data_bucket" {}
variable "source_bucket" {}

provider "google" {
  version = "3.5.0"
  project = var.project
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "your-tfstate-bucket"
    prefix = "gcp-cloudfunction-dataflow-gcs2gcs-tf/tfstat"
  }
}

data "google_project" "project" {
}

resource "google_cloudfunctions_function" "function" {
  name        = "run-replace-text-job-function"
  description = "Run replace-text Dataflow job"
  runtime     = "python37"

  available_memory_mb   = 128
  source_archive_bucket = var.source_bucket
  source_archive_object = "run-replace-text-job-function/src.zip"
  entry_point           = "_dataflow_job_start"
  environment_variables = {
    PROJECTID = var.project
    SOURCE_BUCKET = var.source_bucket
  }
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource = var.data_bucket
  }
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project
  region         = var.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
