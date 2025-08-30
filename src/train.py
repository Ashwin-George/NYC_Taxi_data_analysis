import joblib
from xgboost import XGBRegressor
from .preprocessing import clean_data, feature_engineering, split_data
from .utils import upload_to_s3
import pandas as pd
import os

def train_model(df: pd.DataFrame, model_path="model.pkl", scaler_path="scaler.pkl", bucket=None, prefix=None):
    """Train fare prediction model and save locally + upload to S3"""
    df = clean_data(df)
    X, y, scaler = feature_engineering(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    model = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=6)
    model.fit(X_train, y_train)

    # Save locally
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    # Upload to S3 if provided
    if bucket and prefix:
        upload_to_s3(model_path, bucket, os.path.join(prefix, model_path))
        upload_to_s3(scaler_path, bucket, os.path.join(prefix, scaler_path))

    return model
