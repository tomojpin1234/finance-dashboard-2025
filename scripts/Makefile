PROJECT_ID ?= $(GCP_PROJECT_ID)
DATASET ?= $(BQ_DATASET)
BUCKET_NAME ?= $(BUCKET_NAME)

fetch-worldbank-data:
	poetry run python fetch_worldbank.py

fetch-market-indices:
	poetry run python fetch_market_indices.py

upload-to-gcs:
	poetry run python upload_to_gcs.py

load-to-bigquery-macro-data:
	poetry run python load_to_bigquery.py \
		--bucket $(BUCKET_NAME) \
		--source raw/macro_data.parquet \
		--dataset $(DATASET) \
		--table macro_data \
		--project $(PROJECT_ID)

load-to-bigquery-market-data:
	poetry run python load_to_bigquery.py \
		--bucket $(BUCKET_NAME) \
		--source raw/market_indices.parquet \
		--dataset $(DATASET) \
		--table market_indices \
		--project $(PROJECT_ID)