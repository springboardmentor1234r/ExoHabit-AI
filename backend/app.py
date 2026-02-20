from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
import json
import joblib
scaler = joblib.load("scaler.pkl")

app = Flask(__name__)

# -----------------------------
# Load model
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("cleaned_exoplanet_data.csv", low_memory=False)
# -----------------------------
# Planet name handling (FIXED)
# -----------------------------
if "pl_name" in df.columns:
    df["pl_name"] = df["pl_name"].fillna("Unknown Planet")
    planet_name_col = "pl_name"
else:
    df["pl_name"] = ["Planet-" + str(i) for i in range(len(df))]
    planet_name_col = "pl_name"

# -----------------------------
# Create Habitability Score
# -----------------------------
df["Habitability_Score"] = (
    (1 / (abs(df["pl_eqt"] - 288) + 1)) +
    (1 / (df["pl_radj"] + 1)) +
    (1 / (df["pl_bmassj"] + 1))
)
df["Habitability_Score"] = df["Habitability_Score"].fillna(0).round(3)

# -----------------------------
# Create Habitability Labels (FIXED)
# -----------------------------
df["Habitability_Label"] = pd.cut(
    df["Habitability_Score"],
    bins=[-0.01, 0.5, 1.0, 1.5, 10],
    labels=["Very Low", "Low", "Medium", "High"]
)

# -----------------------------
# Planet name handling
# -----------------------------
planet_name_col = "pl_name" if "pl_name" in df.columns else None
if planet_name_col is None:
    df["planet_id"] = range(1, len(df) + 1)
    planet_name_col = "planet_id"

# -----------------------------
# Store last prediction (GLOBAL)
# -----------------------------
last_prediction = {}

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")

# -----------------------------
# Prediction
# -----------------------------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    global last_prediction

    if request.method == "GET":
        return render_template("predict.html")

    try:
        # -------------------------
        # Read user inputs
        # -------------------------
        pl_radj = float(request.form["pl_radj"])
        pl_bmassj = float(request.form["pl_bmassj"])
        pl_eqt = float(request.form["pl_eqt"])
        st_teff = float(request.form["st_teff"])
        pl_orbper = float(request.form["pl_orbper"])



        # -------------------------
        # Habitability Score
        # -------------------------
        score = (
            (1 / (abs(pl_eqt - 288) + 1)) +
            (1 / (pl_radj + 1)) +
            (1 / (pl_bmassj + 1))
        )
        score = round(score, 3)

        label = "Habitable 🌍" if score >= 1.5 else "Not Habitable ❌"

        confidence = int(min((score / 2.0) * 100, 100))
        # Save for dashboard
        # -------------------------
        last_prediction = {
            "score": score,
            "pl_radj": pl_radj,
            "pl_bmassj": pl_bmassj,
            "label": label
        }

        # -------------------------
        # Top 5 planets (dataset)
        # -------------------------
        top5 = df.sort_values("Habitability_Score", ascending=False).head(5)
        ranking = top5[[planet_name_col, "Habitability_Score"]].to_dict("records")

        return render_template(
            "result.html",
            prediction=label,
            score=score,
            confidence=confidence,
            ranking=ranking,
            name_col=planet_name_col
        )

    except Exception as e:
        return f"Error: {e}"
# -----------------------------
# Rankings Page
# -----------------------------
@app.route("/rankings")
def rankings():
    ranking = df.sort_values(
        by="Habitability_Score", ascending=False
    )[[
            planet_name_col,
            "pl_eqt",
            "pl_orbper",
            "pl_radj",
            "Habitability_Score"
        ]].head(10).to_dict("records")

    return render_template(
        "rankings.html",
        ranking=ranking,
        name_col=planet_name_col
    )

# -----------------------------
# Dashboard Page
# -----------------------------
@app.route("/dashboard")
def dashboard():
    # Dataset stats
    avg_score = round(df["Habitability_Score"].mean(), 2)

    # Scatter plot (dataset)
    scatter_data = [
        {"x": float(r), "y": float(m)}
        for r, m in zip(df["pl_radj"], df["pl_bmassj"])
        if not pd.isna(r) and not pd.isna(m)
    ]
    # -------- Feature Importance --------
    feature_names = [
        "Planet Radius",
        "Planet Mass",
        "Equilibrium Temp",
        "Star Temp",
        "Orbital Period"
    ]

    importances = model.feature_importances_

    feature_importance = [
        {
            "feature": feature_names[i],
            "importance": round(float(importances[i]), 3)
        }
        for i in range(len(importances))
    ]

    # -------- Habitability Distribution --------
    habit_counts = df["Habitability_Label"].value_counts().sort_index()

    habit_labels = habit_counts.index.astype(str).tolist()
    habit_values = habit_counts.values.astype(int).tolist()

    # -------- Scatter Plot (Dataset) --------
    scattered_data = [
        {
            "x": float(row["st_teff"]),
            "y": float(row["Habitability_Score"])
        }
        for _, row in df[["st_teff", "Habitability_Score"]].dropna().iterrows()
    ]

    return render_template(
	"dashboard.html",
        scatter_data=json.dumps(scatter_data),
        user_score=last_prediction.get("score"),
        avg_score=avg_score,
        user_radius=last_prediction.get("pl_radj"),
        user_mass=last_prediction.get("pl_bmassj"),
        user_label=last_prediction.get("label"),
        feature_importance=json.dumps(feature_importance),
        habit_labels=json.dumps(habit_labels),
        habit_values=json.dumps(habit_values),
        scattered_data=json.dumps(scattered_data)
    )

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
