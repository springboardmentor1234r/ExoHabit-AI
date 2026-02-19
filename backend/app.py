from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
import sqlite3

app = Flask(__name__)

# ================= LOAD ML FILES =================
model = joblib.load("models/xgboost_model.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_order = joblib.load("models/feature_order.pkl")

API_KEY = "EXOHABITAI_KEY"

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database/exoplanets.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= HOME PAGE =================
@app.route("/")
def home():
    return render_template("index.html")

# ================= PREDICTION API =================
@app.route("/api/predict", methods=["POST"])
def predict():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    df = pd.DataFrame([data])
    df = df[feature_order]

    df_scaled = scaler.transform(df)
    probs = model.predict_proba(df_scaled)[0]
    pred = int(np.argmax(probs))

    classes = ["Non-Habitable", "Potentially Habitable", "Highly Habitable"]

    return jsonify({
        "prediction": classes[pred],
        "probabilities": {
            "non_habitable": float(probs[0]),
            "potentially_habitable": float(probs[1]),
            "highly_habitable": float(probs[2])
        }
    })

# ================= TOP PLANETS =================
@app.route("/api/top-planets")
def top_planets():
    conn = get_db()
    rows = conn.execute("""
        SELECT pl_name, final_habitability_score
        FROM exoplanets
        ORDER BY final_habitability_score DESC
        LIMIT 10
    """).fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
