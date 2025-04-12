# GCP Setup Instructions for Finance Dashboard Project

This guide documents how to prepare Google Cloud Platform (GCP) for the Finance Dashboard project. It is intended for reviewers or collaborators who want to reproduce or understand the infrastructure setup.

---

## 🛠️ Prerequisites

Before using this project, make sure you have:

- A GCP account with billing enabled
- Access to [Google Cloud Console](https://console.cloud.google.com)
- The Google Cloud SDK (`gcloud`) and Terraform installed locally

---

## 📦 .env File Setup

Create a `.env` file in the **top-level project directory** with the following contents:

```dotenv
GCP_PROJECT_ID=your-project-id
REGION=your-gcp-region
BUCKET_NAME=your-gcs-bucket-name
BQ_DATASET=your-bq-dataset-name
GOOGLE_APPLICATION_CREDENTIALS=../credentials/gcp.json
```

This file is used to:
- Pass variables into Terraform via `Makefile`
- Configure Airflow, dbt, and scripts
- Load GCP credentials

💡 Tip: To use `$GCP_PROJECT_ID` and other variables in gcloud or terraform commands, load the `.env` file into your shell:

```bash
set -a
source .env
set +a
```
Now you can test it:
```bash
gcloud config get-value project --project="$GCP_PROJECT_ID"
# should return:
your-project-id
```


---

## ✅ Manual GCP Setup (One-Time Only)

These steps are required **before running Terraform** or Airflow.

### 1. Create the Project
[https://console.cloud.google.com/projectcreate](https://console.cloud.google.com/projectcreate)

### 2. Link Billing
[https://console.cloud.google.com/billing](https://console.cloud.google.com/billing)

### 3. Enable Required APIs
```bash
gcloud services enable \
  bigquery.googleapis.com \
  storage.googleapis.com \
  iam.googleapis.com \
  cloudresourcemanager.googleapis.com
```

### 4. Create Service Account
```bash
gcloud iam service-accounts create airflow-finance-sa \
  --display-name "Airflow Finance Service Account"
```

### 5. Grant Roles to Service Account
```bash
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:airflow-finance-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
  --member="serviceAccount:airflow-finance-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### 6. Create Credentials (Key File)
```bash
gcloud iam service-accounts keys create ./credentials/gcp.json \
  --iam-account=airflow-finance-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com
```

---

## 🧱 Terraform Setup

Only resources that may be updated over time (GCS bucket, BigQuery dataset) are managed with Terraform.

### 1. Navigate to the Terraform folder
```bash
cd terraform
```

### 2. Run Terraform

```bash
make plan   # Optional dry-run
make apply  # Create or update resources
```

This creates:
- GCS bucket (raw zone)
- BigQuery dataset (for dbt models)

Terraform reads all required variables from your `.env` file.

---

For any issues with GCP setup, make sure:
- The billing account is active
- All required APIs are enabled
- Your service account has proper roles