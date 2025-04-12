import os
from glob import glob

from google.cloud import storage


def upload_file_to_gcs(bucket_name: str, source_path: str, destination_blob: str):
    """
    Upload a local file to GCS.
    """
    print(f"Uploading {source_path} to gs://{bucket_name}/{destination_blob}")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_path)

    print(f"✅ Uploaded {source_path} to GCS as {destination_blob}")


if __name__ == "__main__":
    BUCKET_NAME = "financedashboard-raw-data"
    LOCAL_DIR = "data/raw"
    GCS_PREFIX = "raw/"

    for file in glob(f"{LOCAL_DIR}/*.parquet"):
        filename = os.path.basename(file)
        destination = f"{GCS_PREFIX}{filename}"
        upload_file_to_gcs(BUCKET_NAME, file, destination)
