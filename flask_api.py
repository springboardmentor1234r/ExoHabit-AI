# flask_api_10feat.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# -----------------------------
# Load 10-feature model & scaler
# -----------------------------
model = joblib.load("habitability_model_10feat.pkl")
scaler = joblib.load("scaler_10feat.pkl")

@app.route("/")
def home():
    return "Exoplanet Habitability Prediction API (10-feature) is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Extract 10 features in same order as training
        features = np.array([[
            data["pl_rade"],     # Planet radius
            data["pl_bmasse"],   # Planet mass
            data["pl_orbper"],   # Orbital period
            data["pl_eqt"],      # Equilibrium temp
            data["st_teff"],     # Star temp
            data["st_mass"],     # Star mass
            data["st_rad"],      # Star radius
            data["sy_dist"],     # System distance
            data["pl_insol"],    # Planet insolation flux
            data["st_met"]       # Star metallicity
        ]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Predict
        prediction = model.predict(features_scaled)[0]
        result = "Habitable ✅" if prediction == 1 else "Not Habitable ❌"

        return jsonify({"prediction": int(prediction), "result": result})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
