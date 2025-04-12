# ------------------
# 🧼 Notebook helpers
# ------------------

start-jupyter:
	poetry install --no-root --with test && poetry run python -m ipykernel install --user --name=data-engienering-zoomcamp-project-2 --display-name "Data-Engieneering-Zoomcamp-Project2" \
	tf-init tf-apply tf-destroy


# ------------------------
# 🧪 Python Data Scripts
# ------------------------

SCRIPT_DIR = scripts

script-fetch-worldbank-data:
	cd $(SCRIPT_DIR) && make fetch-worldbank-data

script-fetch-market-indices:
	cd $(SCRIPT_DIR) && make fetch-market-indices

script-upload-to-gcs:
	cd $(SCRIPT_DIR) && make upload-to-gcs

script-load-to-bigquery-macro-data:
	cd $(SCRIPT_DIR) && make load-to-bigquery-macro-data

script-load-to-bigquery-market-data:
	cd $(SCRIPT_DIR) && make load-to-bigquery-market-data

# ------------------
# 🌀 Airflow Commands
# ------------------

AIRFLOW_DIR = airflow

airflow-init:
	cd $(AIRFLOW_DIR) && make init

airflow-up:
	cd $(AIRFLOW_DIR) && make up

airflow-down:
	cd $(AIRFLOW_DIR) && make down

airflow-restart:
	cd $(AIRFLOW_DIR) && make restart

airflow-rebuild:
	cd $(AIRFLOW_DIR) && make rebuild

airflow-logs:
	cd $(AIRFLOW_DIR) && make logs

airflow-trigger:
	cd $(AIRFLOW_DIR) && make trigger

# ------------------
# ☁️ Terraform (optional)
# ------------------

TERRAFORM_DIR = terraform

tf-init:
	$(MAKE) -C terraform init

tf-plan:
	$(MAKE) -C terraform plan

tf-apply:
	$(MAKE) -C terraform apply

tf-destroy:
	$(MAKE) -C terraform destroy	

tf-output-key:
	cd $(TERRAFORM_DIR) && make output-key

# ------------------
# 🧱 DBT Commands
# ------------------

DBT_DIR = ./finance_dashboard_dbt

dbt-run:
	cd $(DBT_DIR) && make run

dbt-run-full:
	cd $(DBT_DIR) && make run-full

dbt-test:
	cd $(DBT_DIR) && make test

dbt-debug:
	cd $(DBT_DIR) && make debug	

# ------------------
# 🧹Utility
# ------------------

clean:
	# rm -rf logs/*
	# rm -rf $(AIRFLOW_DIR)/logs/*
	# rm -rf $(DBT_DIR)/target $(DBT_DIR)/dbt_packages
	rm -rf data/*

setup:
	poetry install --no-root

init:
	mkdir -p data	

reformat:
	poetry run isort airflow/dags/macro_pipeline_dag.py scripts/
	poetry run black airflow/dags/macro_pipeline_dag.py scripts/	