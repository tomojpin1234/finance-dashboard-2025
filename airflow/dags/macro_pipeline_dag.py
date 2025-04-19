import os
import sys
from datetime import datetime, timedelta

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from airflow import DAG

# Add script directory to path for imports
sys.path.append("/opt/airflow")

import os

from scripts.fetch_market_indices import INDEX_SYMBOLS, fetch_index_data

# Import your script functions
from scripts.fetch_worldbank import (
    COUNTRIES,
    INDICATORS,
    fetch_all_data,
    save_to_parquet,
)
from scripts.load_to_bigquery import load_parquet_from_gcs
from scripts.upload_to_gcs import upload_file_to_gcs

BUCKET_NAME = "financedashboard-raw-data"
RAW_DATA_DIR = "/opt/airflow/data/raw"

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")
GCP_KEY_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
LOCATION = os.getenv("REGION", "us-central1")

# Default args
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def upload_all_parquet_to_gcs():
    for file_name in os.listdir(RAW_DATA_DIR):
        if file_name.endswith(".parquet"):
            local_path = os.path.join(RAW_DATA_DIR, file_name)
            destination_blob = f"raw/{file_name}"
            upload_file_to_gcs(BUCKET_NAME, local_path, destination_blob)


with DAG(
    dag_id="macro_data_ingestion",
    default_args=default_args,
    description="Fetch macroeconomic + market data and store as Parquet",
    schedule_interval=None,  # or change to "@once" while testing
    catchup=False,
    tags=["macro", "finance"],
    is_paused_upon_creation=False,
) as dag:

    def task_fetch_macro_data():
        df = fetch_all_data(COUNTRIES, INDICATORS)
        save_to_parquet(df, "data/raw/macro_data.parquet")

    def task_fetch_index_data():
        import pandas as pd

        all_data = []
        for country, symbol in INDEX_SYMBOLS.items():
            df = fetch_index_data(country, symbol)
            all_data.append(df)
        result_df = pd.concat(all_data, ignore_index=True)

        from pyarrow import Table
        from pyarrow import parquet as pq

        result_df["Date"] = pd.to_datetime(result_df["Date"])
        table = Table.from_pandas(result_df)
        pq.write_table(table, "data/raw/market_indices.parquet")

    fetch_macro_data = PythonOperator(
        task_id="fetch_macro_data", python_callable=task_fetch_macro_data
    )

    fetch_market_data = PythonOperator(
        task_id="fetch_market_data", python_callable=task_fetch_index_data
    )

    upload_to_gcs = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_all_parquet_to_gcs,
        dag=dag,
    )

    load_macro_to_bq = PythonOperator(
        task_id="load_macro_data_to_bq",
        python_callable=load_parquet_from_gcs,
        op_kwargs={
            "bucket_name": "financedashboard-raw-data",
            "source_blob": "raw/macro_data.parquet",
            "dataset_id": BQ_DATASET,
            "table_id": "macro_data",
            "project_id": PROJECT_ID,
            "location": LOCATION,
        },
        dag=dag,
    )

    load_market_to_bq = PythonOperator(
        task_id="load_market_data_to_bq",
        python_callable=load_parquet_from_gcs,
        op_kwargs={
            "bucket_name": "financedashboard-raw-data",
            "source_blob": "raw/market_indices.parquet",
            "dataset_id": BQ_DATASET,
            "table_id": "market_indices",
            "project_id": PROJECT_ID,
            "location": LOCATION,
        },
        dag=dag,
    )

    run_dbt = BashOperator(
        task_id="run_dbt_transformations",
        bash_command=(
            "set -e && "
            "cd /opt/airflow/dbt && "
            f"export GOOGLE_APPLICATION_CREDENTIALS={GCP_KEY_PATH} && "
            "dbt run --profiles-dir .dbt"
        ),
        dag=dag,
    )

    dbt_test = BashOperator(
        task_id="run_dbt_tests",
        bash_command="cd /opt/airflow/dbt && dbt test --profiles-dir .dbt",
        dag=dag,
    )

    (
        [fetch_macro_data, fetch_market_data]
        >> upload_to_gcs
        >> [load_macro_to_bq, load_market_to_bq]
        >> run_dbt
        >> dbt_test
    )
