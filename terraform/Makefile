# terraform/Makefile

include ../.env

export TF_VAR_project_id              := $(GCP_PROJECT_ID)
export TF_VAR_region                  := $(REGION)
export TF_VAR_bucket_name             := $(BUCKET_NAME)
export TF_VAR_bq_dataset              := $(BQ_DATASET)
export GOOGLE_APPLICATION_CREDENTIALS := $(GOOGLE_APPLICATION_CREDENTIALS)

.PHONY: init plan apply destroy

init:
	terraform init

plan:
	terraform plan

apply:
	terraform apply -auto-approve

destroy:
	terraform destroy -auto-approve