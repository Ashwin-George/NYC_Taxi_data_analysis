import boto3
import os

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
