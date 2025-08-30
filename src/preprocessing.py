import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: remove nulls, invalid fares, and negative distances"""
    df = df.dropna()
    df = df[df["fare_amount"] > 0]
    df = df[df["trip_distance"] > 0]
    return df

def feature_engineering(df: pd.DataFrame):
    """Create features and split X, y"""
    X = df[["trip_distance", "passenger_count"]]
    y = df["fare_amount"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler

def split_data(X, y, test_size=0.2, random_state=42):
    """Train-test split"""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
