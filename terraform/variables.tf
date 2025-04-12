# terraform/variables.tf

variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "region" {
  type        = string
  description = "GCP Region"
}

variable "bucket_name" {
  type        = string
  description = "GCS Bucket for raw data"
}

variable "bq_dataset" {
  type        = string
  description = "BigQuery dataset name"
}