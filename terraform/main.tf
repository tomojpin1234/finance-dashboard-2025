# terraform/main.tf

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "raw_data" {
  name                        = var.bucket_name
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "finance_dashboard" {
  dataset_id                   = var.bq_dataset
  location                     = var.region
  default_table_expiration_ms = null
}

output "bucket_name" {
  value = google_storage_bucket.raw_data.name
}

output "bq_dataset_id" {
  value = google_bigquery_dataset.finance_dashboard.dataset_id
}