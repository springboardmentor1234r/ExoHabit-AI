from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

# -----------------------------
# Load trained ML model
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))

# -----------------------------
# Load cleaned dataset
# -----------------------------
df = pd.read_csv("cleaned_exoplanet_data.csv", low_memory=False)

# -----------------------------
# Ensure Habitability_Score exists
# -----------------------------
if "Habitability_Score" not in df.columns:
    df["Habitability_Score"] = (
        (1 / (abs(df["pl_eqt"] - 288) + 1)) +
        (1 / (df["pl_radj"] + 1)) +
        (1 / (df["pl_bmassj"] + 1))
    )

# -----------------------------
# Detect planet name column safely
# -----------------------------
possible_name_cols = ["pl_name", "pl_hostname", "hostname", "name"]
planet_name_col = None

for col in possible_name_cols:
    if col in df.columns:
        planet_name_col = col
        break

# If no name column exists, create an ID
if planet_name_col is None:
    df["planet_id"] = range(1, len(df) + 1)
    planet_name_col = "planet_id"

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
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
        # ML prediction
        # -------------------------
        input_data = np.array([[pl_radj, pl_bmassj, pl_eqt, st_teff, pl_orbper]])
        prediction = model.predict(input_data)[0]
        probability = round(model.predict_proba(input_data)[0][1], 3)

        # -------------------------
        # Habitability Score
        # -------------------------
        habitability_score = (
            (1 / (abs(pl_eqt - 288) + 1)) +
            (1 / (pl_radj + 1)) +
            (1 / (pl_bmassj + 1))
        )

        habitability_score = round(habitability_score, 3)

        label = "Habitable 🌍" if habitability_score >= 1.5 else "Not Habitable ❌"

        # -------------------------
        # Top 5 ranking
        # -------------------------
        top_planets = df.sort_values(
            by="Habitability_Score", ascending=False
        ).head(5)

        ranking = top_planets[
            [planet_name_col, "Habitability_Score"]
        ].to_dict(orient="records")

        return render_template(
            "result.html",
            prediction=label,
            score=habitability_score,
            confidence=probability,
            ranking=ranking,
            name_col=planet_name_col
        )

    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
