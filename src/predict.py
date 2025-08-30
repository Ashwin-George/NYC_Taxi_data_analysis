import joblib
import numpy as np

def load_model(model_path="model.pkl", scaler_path="scaler.pkl"):
    """Load model + scaler"""
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict_fare(trip_distance: float, passenger_count: int, model_path="model.pkl", scaler_path="scaler.pkl"):
    """Predict taxi fare"""
    model, scaler = load_model(model_path, scaler_path)
    features = np.array([[trip_distance, passenger_count]])
    features_scaled = scaler.transform(features)
    return float(model.predict(features_scaled)[0])
