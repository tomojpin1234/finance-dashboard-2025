# Makefile for dbt project

include ../.env

GOOGLE_APPLICATION_CREDENTIALS ?= $(GOOGLE_APPLICATION_CREDENTIALS)
GCP_PROJECT_ID ?= $(GCP_PROJECT_ID)
BQ_DATASET ?= $(BQ_DATASET)
REGION ?= $(REGION)

DBT_PROFILES_DIR := .dbt

# Base env setup
ENV_EXPORT = \
	GCP_PROJECT_ID=$(GCP_PROJECT_ID) \
	BQ_DATASET=$(BQ_DATASET) \
	REGION=$(REGION) \
	GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS)

# Run all dbt commands with env context
DBT_RUN         = $(ENV_EXPORT) poetry run dbt run --profiles-dir $(DBT_PROFILES_DIR)
DBT_RUN_FULL    = $(ENV_EXPORT) poetry run dbt run --full-refresh --profiles-dir $(DBT_PROFILES_DIR)
DBT_TEST        = $(ENV_EXPORT) poetry run dbt test --profiles-dir $(DBT_PROFILES_DIR)
DBT_DOCS_GEN    = $(ENV_EXPORT) poetry run dbt docs generate --profiles-dir $(DBT_PROFILES_DIR)
DBT_DOCS_SERVE  = $(ENV_EXPORT) poetry run dbt docs serve --profiles-dir $(DBT_PROFILES_DIR)
DBT_DEBUG       = $(ENV_EXPORT) poetry run dbt debug --profiles-dir $(DBT_PROFILES_DIR)

# Default target
all: run

debug:
	$(DBT_DEBUG)

run:
	$(DBT_RUN)

run-full:
	$(DBT_RUN_FULL)

test:
	$(DBT_TEST)

docs:
	$(DBT_DOCS_GEN)
	$(DBT_DOCS_SERVE)

clean:
	rm -rf target