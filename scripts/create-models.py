import pandas as pd
import os
from src.train import train_model

if __name__ == "__main__":
    # 🔹 Environment vars from GitHub Secrets
    BUCKET = os.getenv("S3_BUCKET")
    PREFIX = "models/nyc_taxi"

    # 🔹 Fetch training data from S3
    DATA_PATH = "taxi_data.csv"
    os.system(f"aws s3 cp s3://{BUCKET}/raw/{DATA_PATH} {DATA_PATH}")

    print("📥 Data downloaded, starting preprocessing & training...")
    df = pd.read_csv(DATA_PATH)

    # 🔹 Train model & upload to S3
    train_model(df, model_path="model.pkl", scaler_path="scaler.pkl",
                bucket=BUCKET, prefix=PREFIX)

    print("✅ Initial model created and uploaded to S3!")
