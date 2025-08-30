import boto3
import os
import json
from datetime import datetime

def upload_to_s3(file_path, bucket, key):
    """Upload file to S3"""
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket, key)
    print(f"✅ Uploaded {file_path} to s3://{bucket}/{key}")

def download_from_s3(bucket, key, local_path):
    """Download file from S3"""
    s3 = boto3.client("s3")
    s3.download_file(bucket, key, local_path)
    print(f"⬇️ Downloaded {key} to {local_path}")
    return local_path

def save_metadata(row_count: int, bucket: str, prefix: str, filename="metadata.json"):
    """Create metadata.json and upload to S3"""
    metadata = {
        "row_count": row_count,
        "last_trained": datetime.utcnow().isoformat() + "Z"
    }

    local_path = filename
    with open(local_path, "w") as f:
        json.dump(metadata, f, indent=2)

    upload_to_s3(local_path, bucket, os.path.join(prefix, filename))
    print(f"✅ Metadata saved to s3://{bucket}/{prefix}/{filename}")
