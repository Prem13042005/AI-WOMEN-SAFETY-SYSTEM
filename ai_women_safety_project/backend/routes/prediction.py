from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import datetime
import os

prediction_routes = Blueprint('prediction_routes', __name__)

# Resolve dynamic path to the models folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))         # /backend/routes
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')           # /backend/models
model_path = os.path.join(MODELS_DIR, 'danger_predictor.pkl')
scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')

# Load model and scaler safely
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("✅ AI Model & Scaler loaded successfully.")
except Exception as load_error:
    print(f"❌ Error loading model or scaler: {load_error}")
    model = None
    scaler = None

# Dummy logic — replace with GPS-based classification in production
def get_location_type(lat, lon):
    if lat > 18.55:
        return 0  # Urban
    elif lat > 18.5:
        return 1  # Semi-urban
    else:
        return 2  # Slum/Isolated

@prediction_routes.route('/danger_level', methods=['POST'])
def predict_risk():
    if model is None or scaler is None:
        return jsonify({
            'status': 'error',
            'message': 'AI model or scaler not loaded.'
        }), 500

    try:
        data = request.get_json()
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        timestamp = data.get('timestamp') or datetime.datetime.now().isoformat()

        if latitude == 0 or longitude == 0:
            return jsonify({'status': 'error', 'message': 'Missing or invalid coordinates'}), 400

        dt = datetime.datetime.fromisoformat(timestamp)
        hour = dt.hour
        is_night = 1 if hour < 6 or hour >= 21 else 0
        day_of_week = dt.weekday()
        location_type = get_location_type(latitude, longitude)

        features = np.array([[latitude, longitude, hour, is_night, day_of_week, location_type]])
        scaled = scaler.transform(features)

        risk_level = int(model.predict(scaled)[0])
        confidence = max(model.predict_proba(scaled)[0])

        return jsonify({
            'status': 'success',
            'risk_level': risk_level,
            'confidence': round(confidence, 3),
            'details': {
                'hour': hour,
                'night_time': bool(is_night),
                'day_of_week': day_of_week,
                'location_type': location_type
            }
        }), 200

    except Exception as e:
        print("❌ Prediction Exception:", e)
        return jsonify({'status': 'error', 'message': 'Prediction failed', 'error': str(e)}), 500
