from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Load trained model (safe absolute path)
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "processed",
    "logistic_regression_model.pkl"
)

model = joblib.load(MODEL_PATH)

@app.route("/")
def home():
    return "ExoHabit-AI Backend is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "pl_rade" not in data:
        return jsonify({"error": "pl_rade value is required"}), 400

    pl_rade = float(data["pl_rade"])

    input_data = np.array([[pl_rade]])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return jsonify({
        "planet_radius": pl_rade,
        "habitable": int(prediction),
        "habitability_probability": round(float(probability), 3)
    })

if __name__ == "__main__":
    app.run(debug=True)
