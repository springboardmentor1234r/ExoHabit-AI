from flask import Flask, request, render_template
import joblib
import numpy as np
import os
import json

app = Flask(__name__)

# ==============================
# Load Trained Model
# ==============================
model_path = os.path.join(os.path.dirname(__file__), "../models/habitability_model.pkl")
model = joblib.load(model_path)

# ==============================
# Utility: Validate Inputs
# ==============================
def validate_inputs(form_data):
    required_fields = [
        "pl_orbper", "pl_orbsmax", "pl_bmasse",
        "pl_eqt", "st_teff", "st_rad",
        "st_mass", "st_lum"
    ]

    for field in required_fields:
        if field not in form_data or form_data[field] == "":
            return False, f"Missing value for {field}"

    return True, None

# ==============================
# Utility: Prepare Features
# ==============================
def prepare_features(form_data):
    pl_orbper = float(form_data["pl_orbper"])
    pl_orbsmax = float(form_data["pl_orbsmax"])
    pl_bmasse = float(form_data["pl_bmasse"])
    pl_eqt = float(form_data["pl_eqt"])
    st_teff = float(form_data["st_teff"])
    st_rad = float(form_data["st_rad"])
    st_mass = float(form_data["st_mass"])
    st_lum = float(form_data["st_lum"])

    pl_rade = pl_bmasse ** (1/3)
    pl_insol = st_lum / (pl_orbsmax ** 2) if pl_orbsmax > 0 else 0

    features = np.array([[ 
        pl_orbper, pl_orbsmax, pl_bmasse,
        pl_eqt, st_teff, st_rad,
        st_mass, st_lum,
        pl_rade, pl_insol
    ]])

    return features

# ==============================
# Utility: Generate Prediction
# ==============================
def generate_prediction(features):
    probability = model.predict_proba(features)[0][1]
    score_percentage = round(probability * 100, 1)

    if score_percentage >= 50:
        classification = "Potentially Habitable 🌍"
    else:
        classification = "Not Habitable ❌"

    if score_percentage >= 65:
        ranking = "Highly Earth-like Candidate ⭐⭐⭐⭐"
        explanation = "Strong planetary and stellar alignment detected."
    elif score_percentage >= 55:
        ranking = "Strong Habitability Candidate ⭐⭐⭐"
        explanation = "Favorable environmental parameters observed."
    elif score_percentage >= 50:
        ranking = "Moderately Promising ⭐⭐"
        explanation = "Above-average habitability likelihood."
    elif score_percentage >= 40:
        ranking = "Weak Habitability Signals ⭐"
        explanation = "Marginal environmental suitability."
    else:
        ranking = "Unfavorable Conditions"
        explanation = "Extreme temperature or radiation exposure reduces habitability potential."

    confidence_strength = round(abs(score_percentage - 50) * 2, 1)

    if confidence_strength >= 60:
        confidence_label = "High Confidence"
    elif confidence_strength >= 30:
        confidence_label = "Moderate Confidence"
    else:
        confidence_label = "Low Confidence"

    feature_names = [
        "Orbital Period", "Semi-Major Axis", "Planet Mass",
        "Equilibrium Temperature", "Star Temperature",
        "Star Radius", "Star Mass", "Star Luminosity",
        "Planet Radius (Derived)", "Insolation (Derived)"
    ]

    importances = model.feature_importances_
    top_indices = np.argsort(importances)[-3:][::-1]
    top_features = [feature_names[i] for i in top_indices]
    feature_explanation = "Prediction influenced mainly by: " + ", ".join(top_features)

    return {
        "score": score_percentage,
        "classification": classification,
        "ranking": ranking,
        "explanation": explanation,
        "confidence_label": confidence_label,
        "confidence_strength": confidence_strength,
        "feature_explanation": feature_explanation
    }

# ==============================
# Routes
# ==============================

@app.route("/")
def home():
    return render_template("predict.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/exoplanets")
def exoplanets():
    return render_template("exoplanets.html")

@app.route("/solar-system")
def solar_system():
    return render_template("solar_system.html")

@app.route("/dashboard")
def dashboard():
    try:
        metrics_path = os.path.join(os.path.dirname(__file__), "../models/model_metrics.json")

        with open(metrics_path, "r") as f:
            metrics = json.load(f)

        return render_template(
            "dashboard.html",
            accuracy=round(metrics["accuracy"] * 100, 2),
            precision=round(metrics["precision"] * 100, 2),
            recall=round(metrics["recall"] * 100, 2),
            f1_score=round(metrics["f1_score"] * 100, 2),
            roc_auc=round(metrics["roc_auc"] * 100, 2),
            tn=metrics["true_negative"],
            fp=metrics["false_positive"],
            fn=metrics["false_negative"],
            tp=metrics["true_positive"],
            total=metrics["total_samples"]
        )

    except Exception as e:
        return f"Dashboard Error: {str(e)}"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        valid, error_message = validate_inputs(request.form)
        if not valid:
            return f"Input Error: {error_message}"

        features = prepare_features(request.form)
        result = generate_prediction(features)

        return render_template(
            "predict.html",
            prediction_text=result["classification"],
            score=result["score"],
            ranking=result["ranking"],
            explanation=result["explanation"],
            confidence_label=result["confidence_label"],
            confidence_strength=result["confidence_strength"],
            feature_explanation=result["feature_explanation"]
        )

    except Exception as e:
        return f"Server Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
