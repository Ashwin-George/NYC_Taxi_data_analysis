import pandas as pd
import os
from src.train import train_model
from src.utils import download_from_s3

if __name__ == "__main__":
    # 🔹 Environment vars
    BUCKET = os.getenv("S3_BUCKET")
    PREFIX = "models/nyc_taxi"

    # 🔹 Fetch latest dataset from S3
    DATA_PATH = "taxi_data.csv"
    os.system(f"aws s3 cp s3://{BUCKET}/raw/{DATA_PATH} {DATA_PATH}")

    print("📥 Latest data downloaded for retraining...")
    df = pd.read_csv(DATA_PATH)

    # 🔹 Retrain & overwrite model in S3
    train_model(df, model_path="model.pkl", scaler_path="scaler.pkl",
                bucket=BUCKET, prefix=PREFIX)

    print("♻️ Model retrained and updated in S3!")
