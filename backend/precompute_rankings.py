"""
precompute_rankings.py - Precomputes habitability rankings and dashboard data.

Run this AFTER export_model.py to generate:
  - models/rankings.csv
  - models/dashboard_data.json

Usage:
  python precompute_rankings.py
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# ============================================================
# Load assets
# ============================================================
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

rf_model = joblib.load(os.path.join(MODEL_DIR, 'habitability_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
num_imputer = joblib.load(os.path.join(MODEL_DIR, 'num_imputer.pkl'))
cat_imputer = joblib.load(os.path.join(MODEL_DIR, 'cat_imputer.pkl'))
train_features = joblib.load(os.path.join(MODEL_DIR, 'train_features.pkl'))
star_categories = joblib.load(os.path.join(MODEL_DIR, 'star_categories.pkl'))

# ============================================================
# Load and preprocess full dataset
# ============================================================
print("Loading dataset...")
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'Exoplanet_habitability_dataset.csv'), comment='#')

features = [
    'pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_masse',
    'pl_dens', 'pl_insol', 'pl_eqt', 'st_teff',
    'st_met', 'st_lum', 'st_spectype'
]
df_clean = df[features].copy()

# Clean
df_clean['st_spectype'] = df_clean['st_spectype'].str[0]
num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
df_clean[num_cols] = num_imputer.transform(df_clean[num_cols])
df_clean[['st_spectype']] = cat_imputer.transform(df_clean[['st_spectype']])

for col in num_cols:
    lower, upper = df_clean[col].quantile([0.01, 0.99])
    df_clean[col] = df_clean[col].clip(lower, upper)

# Feature engineering
def calc_hab(row):
    return (
        np.exp(-abs(row['pl_rade'] - 1.0) / 1.0) *
        np.exp(-abs(row['pl_dens'] - 5.51) / 5.0) *
        np.exp(-abs(row['pl_eqt'] - 255.0) / 50.0) *
        np.exp(-abs(row['pl_insol'] - 1.0) / 1.0)
    ) ** (1/4)

def calc_stellar(row):
    return (
        np.exp(-abs(row['st_teff'] - 5778) / 1000.0) *
        np.exp(-abs(row['st_lum'] - 0.0) / 1.0) *
        np.exp(-abs(row['st_met'] - 0.0) / 0.5)
    ) ** (1/3)

df_clean['habitability_score'] = df_clean.apply(calc_hab, axis=1)
df_clean['stellar_compatibility'] = df_clean.apply(calc_stellar, axis=1)

# Save star type before encoding
star_col = df_clean['st_spectype'].copy()

# One-hot encode
df_clean = pd.get_dummies(df_clean, columns=['st_spectype'], prefix='star_type')

# Align columns
for col in train_features:
    if col not in df_clean.columns:
        df_clean[col] = 0
df_clean = df_clean[train_features]

# Scale
X_scaled = scaler.transform(df_clean)

# ============================================================
# Predict and rank
# ============================================================
print("Computing predictions...")
probs = rf_model.predict_proba(X_scaled)[:, 1]

rankings = pd.DataFrame({
    'rank': range(1, len(probs) + 1),
    'original_index': df.index,
    'probability': probs,
    'pl_orbper': df[features[0]],
    'pl_rade': df['pl_rade'],
    'pl_eqt': df['pl_eqt'],
    'st_teff': df['st_teff'],
    'st_spectype': star_col.values,
})

rankings = rankings.sort_values('probability', ascending=False).reset_index(drop=True)
rankings['rank'] = range(1, len(rankings) + 1)

rankings.to_csv(os.path.join(MODEL_DIR, 'rankings.csv'), index=False)
print(f"✅ Rankings saved ({len(rankings)} rows)")

# ============================================================
# Dashboard data
# ============================================================
print("Computing dashboard data...")

# Habitability score distribution
hab_scores = df_clean_orig = df[features].copy() if 'habitability_score' not in df.columns else df
# Recompute from original
scores = []
df_temp = df[features].copy()
df_temp['st_spectype'] = df_temp['st_spectype'].str[0]
num_c = df_temp.select_dtypes(include=[np.number]).columns.tolist()
df_temp[num_c] = num_imputer.transform(df_temp[num_c])
df_temp[['st_spectype']] = cat_imputer.transform(df_temp[['st_spectype']])
for col in num_c:
    l, u = df_temp[col].quantile([0.01, 0.99])
    df_temp[col] = df_temp[col].clip(l, u)
df_temp['hab_score'] = df_temp.apply(calc_hab, axis=1)

bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
labels = [f"{b:.1f}-{bins[i+1]:.1f}" for i, b in enumerate(bins[:-1])]
df_temp['hab_bin'] = pd.cut(df_temp['hab_score'], bins=bins, labels=labels, include_lowest=True)
hab_dist = df_temp['hab_bin'].value_counts().sort_index().to_dict()

# Star type distribution
star_dist = star_col.value_counts().to_dict()

# Feature importance
importances = rf_model.feature_importances_
feature_imp = sorted(
    zip(train_features, importances.tolist()),
    key=lambda x: x[1], reverse=True
)

dashboard = {
    'habitability_distribution': [{'range': k, 'count': int(v)} for k, v in hab_dist.items()],
    'star_type_distribution': [{'type': k, 'count': int(v)} for k, v in sorted(star_dist.items())],
    'feature_importance': [{'feature': f, 'importance': round(imp, 4)} for f, imp in feature_imp],
    'total_planets': len(df),
    'habitable_count': int((probs > 0.5).sum()),
}

with open(os.path.join(MODEL_DIR, 'dashboard_data.json'), 'w') as f:
    json.dump(dashboard, f, indent=2)

print("✅ Dashboard data saved")
print(f"   Total planets: {dashboard['total_planets']}")
print(f"   Predicted habitable: {dashboard['habitable_count']}")
