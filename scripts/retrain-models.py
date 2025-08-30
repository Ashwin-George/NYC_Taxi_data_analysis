# scripts/retrain_models.py

import json
import os
import pandas as pd
from src.train import train_model
from src.utils import download_from_s3, upload_to_s3

# Config    # 🔹 Fetch training data from S3
#     S3_DATA_PATH = "yellow_tripdata-part-6.csv"
#     DATA_PATH = "taxi_data.csv"
#     os.system(f"aws s3 cp s3://{BUCKET}/data/{S3_DATA_PATH} {DATA_PATH}")
BUCKET = os.getenv("S3_BUCKET")
PREFIX = os.getenv("S3_PREFIX", "models/")
DATA_KEY = os.getenv("DATA_KEY", "data/nyc_taxi_data.parquet")
METADATA_KEY = os.path.join(PREFIX, "metadata.json")
RETRAIN_THRESHOLD = 50000  # rows to trigger retraining

def load_metadata():
    """Load model metadata (row count, last trained) from S3"""
    try:
        download_from_s3(BUCKET, METADATA_KEY, "metadata.json")
        with open("metadata.json", "r") as f:
            return json.load(f)
    except Exception:
        return {"last_row_count": 0, "last_trained": None}

def save_metadata(row_count):
    """Save updated metadata back to S3"""
    metadata = {"last_row_count": row_count, "last_trained": pd.Timestamp.now().isoformat()}
    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    upload_to_s3("metadata.json", BUCKET, METADATA_KEY)

def retrain_if_needed():
    # 1. Download latest dataset
    local_file = "latest_data.parquet"
    download_from_s3(BUCKET, DATA_KEY, local_file)
    df = pd.read_parquet(local_file)

    # 2. Load metadata
    metadata = load_metadata()
    prev_count = metadata.get("last_row_count", 0)

    # 3. Check threshold
    new_rows = len(df) - prev_count
    print(f"Previous rows: {prev_count}, Current rows: {len(df)}, New rows: {new_rows}")

    if new_rows >= RETRAIN_THRESHOLD:
        print("Threshold reached. Retraining model...")
        train_model(df, model_path="model.pkl", scaler_path="scaler.pkl", bucket=BUCKET, prefix=PREFIX)
        save_metadata(len(df))
        print("✅ Model retrained and uploaded.")
    else:
        print("Not enough new data to retrain. Skipping.")

if __name__ == "__main__":
    retrain_if_needed()
