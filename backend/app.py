"""
app.py - Flask web application for Exoplanet Habitability Prediction.

Endpoints:
  POST /predict         - Predict habitability for a single exoplanet
  GET  /rankings        - Get top habitable exoplanet candidates
  GET  /features        - Get the list of input features
  GET  /feature-importance - Get feature importance from the model
  GET  /dashboard-data  - Get aggregated data for the dashboard
"""

import os
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ============================================================
# Load Model Assets
# ============================================================
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

rf_model = joblib.load(os.path.join(MODEL_DIR, 'habitability_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
num_imputer = joblib.load(os.path.join(MODEL_DIR, 'num_imputer.pkl'))
cat_imputer = joblib.load(os.path.join(MODEL_DIR, 'cat_imputer.pkl'))
train_features = joblib.load(os.path.join(MODEL_DIR, 'train_features.pkl'))
star_categories = joblib.load(os.path.join(MODEL_DIR, 'star_categories.pkl'))

# Load precomputed rankings if available
RANKINGS_PATH = os.path.join(MODEL_DIR, 'rankings.csv')
rankings_df = pd.read_csv(RANKINGS_PATH) if os.path.exists(RANKINGS_PATH) else None

# Load precomputed dashboard data if available
DASHBOARD_PATH = os.path.join(MODEL_DIR, 'dashboard_data.json')
dashboard_data = None
if os.path.exists(DASHBOARD_PATH):
    import json
    with open(DASHBOARD_PATH) as f:
        dashboard_data = json.load(f)

print("✅ Model assets loaded successfully.")

# ============================================================
# Helper: Preprocess a single input
# ============================================================
RAW_NUM_COLS = ['pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_masse',
                'pl_dens', 'pl_insol', 'pl_eqt', 'st_teff', 'st_met', 'st_lum']

def preprocess_input(data: dict) -> pd.DataFrame:
    """Transform raw input dict into model-ready feature vector."""
    # Build raw dataframe
    row = {}
    for col in RAW_NUM_COLS:
        row[col] = float(data.get(col, np.nan))
    row['st_spectype'] = str(data.get('st_spectype', '')).strip()[:1].upper()

    df = pd.DataFrame([row])

    # Impute numerical
    df[RAW_NUM_COLS] = num_imputer.transform(df[RAW_NUM_COLS])

    # Impute categorical
    if df['st_spectype'].iloc[0] == '' or pd.isna(df['st_spectype'].iloc[0]):
        df[['st_spectype']] = cat_imputer.transform(df[['st_spectype']])

    # Feature engineering
    r = df.iloc[0]
    hab_score = (
        np.exp(-abs(r['pl_rade'] - 1.0) / 1.0) *
        np.exp(-abs(r['pl_dens'] - 5.51) / 5.0) *
        np.exp(-abs(r['pl_eqt'] - 255.0) / 50.0) *
        np.exp(-abs(r['pl_insol'] - 1.0) / 1.0)
    ) ** (1/4)

    stellar_compat = (
        np.exp(-abs(r['st_teff'] - 5778) / 1000.0) *
        np.exp(-abs(r['st_lum'] - 0.0) / 1.0) *
        np.exp(-abs(r['st_met'] - 0.0) / 0.5)
    ) ** (1/3)

    df['habitability_score'] = hab_score
    df['stellar_compatibility'] = stellar_compat

    # One-hot encode st_spectype
    spec = df['st_spectype'].iloc[0]
    df = df.drop(columns=['st_spectype'])
    for cat in star_categories:
        df[f'star_type_{cat}'] = 1 if spec == cat else 0

    # Ensure correct column order, filling missing with 0
    for col in train_features:
        if col not in df.columns:
            df[col] = 0
    df = df[train_features]

    # Scale
    df_scaled = pd.DataFrame(scaler.transform(df), columns=train_features)
    return df_scaled, hab_score, stellar_compat


# ============================================================
# Routes
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Predict habitability for a single exoplanet."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        df_scaled, hab_score, stellar_compat = preprocess_input(data)
        
        prob = rf_model.predict_proba(df_scaled)[0]
        prediction = int(rf_model.predict(df_scaled)[0])

        return jsonify({
            'prediction': 'Potentially Habitable' if prediction == 1 else 'Not Habitable',
            'probability': round(float(prob[1]), 4),
            'habitability_score': round(float(hab_score), 4),
            'stellar_compatibility': round(float(stellar_compat), 4),
            'class': prediction,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/rankings', methods=['GET'])
def rankings():
    """Return top habitable exoplanet candidates."""
    if rankings_df is None:
        return jsonify({'error': 'Rankings not precomputed. Run precompute_rankings.py first.'}), 404

    top_n = request.args.get('top', 20, type=int)
    top = rankings_df.head(min(top_n, len(rankings_df)))
    return jsonify(top.to_dict(orient='records'))


@app.route('/features', methods=['GET'])
def features():
    """Return the list of input features expected by the model."""
    return jsonify({
        'raw_features': RAW_NUM_COLS + ['st_spectype'],
        'star_categories': star_categories,
        'model_features': train_features,
    })


@app.route('/feature-importance', methods=['GET'])
def feature_importance():
    """Return feature importance scores from the Random Forest."""
    importances = rf_model.feature_importances_
    feature_imp = sorted(
        zip(train_features, importances.tolist()),
        key=lambda x: x[1], reverse=True
    )
    return jsonify([
        {'feature': f, 'importance': round(imp, 4)}
        for f, imp in feature_imp
    ])


@app.route('/dashboard-data', methods=['GET'])
def dashboard_data_endpoint():
    """Return precomputed dashboard data."""
    if dashboard_data is None:
        return jsonify({'error': 'Dashboard data not precomputed. Run precompute_rankings.py first.'}), 404
    return jsonify(dashboard_data)


# ============================================================
# Run
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
