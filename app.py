from flask import Flask, request, jsonify
import os
import joblib
import numpy as np
from src.utils import download_from_s3

app = Flask(__name__)

# --- S3 Configuration ---
S3_BUCKET = os.getenv("S3_BUCKET", "nyc.archive.data.storage")
S3_PREFIX = os.getenv("S3_PREFIX", "models/nyc_taxi/")
MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"

# --- Load model from S3 if not cached ---
def load_model_from_s3():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("🔄 Downloading model and scaler from S3...")
        download_from_s3(S3_BUCKET, os.path.join(S3_PREFIX, MODEL_PATH), MODEL_PATH)
        download_from_s3(S3_BUCKET, os.path.join(S3_PREFIX, SCALER_PATH), SCALER_PATH)
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "NYC Taxi Fare Prediction API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    """POST JSON like:
    {
        "trip_distance": 3.2,
        "passenger_count": 2
    }
    """
    try:
        data = request.get_json()
        trip_distance = float(data.get("trip_distance"))
        passenger_count = int(data.get("passenger_count"))

        model, scaler = load_model_from_s3()
        features = np.array([[trip_distance, passenger_count]])
        features_scaled = scaler.transform(features)
        prediction = float(model.predict(features_scaled)[0])

        return jsonify({
            "predicted_fare": round(prediction, 2),
            "trip_distance": trip_distance,
            "passenger_count": passenger_count
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
