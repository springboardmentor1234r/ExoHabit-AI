from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__, template_folder="../frontend/templates")

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        data["pl_rade"],
        data["pl_bmasse"],
        data["pl_dens"],
        data["pl_eqt"],
        data["pl_orbper"],
        data["st_teff"],
        data["st_lum"],
        data["st_met"]
    ]])

    features_scaled = scaler.transform(features)
    prob = model.predict_proba(features_scaled)[0][1]

    return jsonify({
        "habitability_probability": round(float(prob), 3),
        "prediction": "Habitable" if prob >= 0.6 else "Non-Habitable"
    })

if __name__ == "__main__":
    app.run(debug=True)
