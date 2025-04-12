import argparse
import os

from google.cloud import bigquery


def load_parquet_from_gcs(
    bucket_name: str,
    source_blob: str,
    dataset_id: str,
    table_id: str,
    project_id: str,
    location: str = "europe-central2",
):
    """
    Load a Parquet file from GCS into a BigQuery table
    """
    client = bigquery.Client(project=project_id)

    # Construct GCS URI
    uri = f"gs://{bucket_name}/{source_blob}"
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    print(f"Starting load job for {full_table_id} from {uri}...")

    load_job = client.load_table_from_uri(
        uri, full_table_id, location=location, job_config=job_config
    )

    load_job.result()  # Wait for job to complete

    table = client.get_table(full_table_id)
    print(f"✅ Loaded {table.num_rows} rows into {full_table_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load Parquet file from GCS into BigQuery"
    )
    parser.add_argument("--bucket", required=True, help="GCS bucket name")
    parser.add_argument("--source", required=True, help="Source blob path in GCS")
    parser.add_argument("--dataset", required=True, help="BigQuery dataset ID")
    parser.add_argument("--table", required=True, help="BigQuery table ID")
    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument(
        "--location", default="europe-central2", help="BigQuery location"
    )

    args = parser.parse_args()

    load_parquet_from_gcs(
        bucket_name=args.bucket,
        source_blob=args.source,
        dataset_id=args.dataset,
        table_id=args.table,
        project_id=args.project,
        location=args.location,
    )
