"""
export_model.py - Recreates the ML pipeline from the notebook and saves all model assets.

Usage:
  1. Place 'Exoplanet_habitability_dataset.csv' in the same directory.
  2. Run: python export_model.py
  3. All model assets will be saved to the /models directory.
"""

import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# ============================================================
# 1. Load Data
# ============================================================
print("Loading data...")
df = pd.read_csv('../data/raw/Exoplanet_habitability_dataset.csv', comment='#')

features = [
    'pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_masse',
    'pl_dens', 'pl_insol', 'pl_eqt', 'st_teff',
    'st_met', 'st_lum', 'st_spectype'
]
df_clean = df[features].copy()
print(f"Data loaded with {df_clean.shape[0]} rows.")

# ============================================================
# 2. Clean & Impute
# ============================================================
# Simplify star type to first letter (spectral class)
df_clean['st_spectype'] = df_clean['st_spectype'].str[0]

# Identify column types
num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()

# Impute numerical columns (median)
num_imputer = SimpleImputer(strategy='median')
df_clean[num_cols] = num_imputer.fit_transform(df_clean[num_cols])

# Impute categorical column (most frequent)
cat_imputer = SimpleImputer(strategy='most_frequent')
df_clean[['st_spectype']] = cat_imputer.fit_transform(df_clean[['st_spectype']])

# Clip outliers to 1st and 99th percentiles
for col in num_cols:
    lower, upper = df_clean[col].quantile([0.01, 0.99])
    df_clean[col] = df_clean[col].clip(lower, upper)

print("Data cleaning complete.")

# ============================================================
# 3. Feature Engineering
# ============================================================
def calculate_hab_score(row):
    s_radius = np.exp(-abs(row['pl_rade'] - 1.0) / 1.0)
    s_density = np.exp(-abs(row['pl_dens'] - 5.51) / 5.0)
    s_temp = np.exp(-abs(row['pl_eqt'] - 255.0) / 50.0)
    s_insol = np.exp(-abs(row['pl_insol'] - 1.0) / 1.0)
    return (s_radius * s_density * s_temp * s_insol) ** (1/4)

def calculate_stellar_index(row):
    t_sim = np.exp(-abs(row['st_teff'] - 5778) / 1000.0)
    l_sim = np.exp(-abs(row['st_lum'] - 0.0) / 1.0)
    m_sim = np.exp(-abs(row['st_met'] - 0.0) / 0.5)
    return (t_sim * l_sim * m_sim) ** (1/3)

df_clean['habitability_score'] = df_clean.apply(calculate_hab_score, axis=1)
df_clean['stellar_compatibility'] = df_clean.apply(calculate_stellar_index, axis=1)
print("Feature engineering complete.")

# ============================================================
# 4. Define Target
# ============================================================
df_clean['target'] = (df_clean['habitability_score'] > 0.5).astype(int)

# ============================================================
# 5. One-Hot Encode Star Type
# ============================================================
# Save the categories seen before encoding
star_categories = sorted(df_clean['st_spectype'].unique().tolist())
df_clean = pd.get_dummies(df_clean, columns=['st_spectype'], prefix='star_type')

# ============================================================
# 6. Prepare Features & Target
# ============================================================
X = df_clean.drop(columns=['target'])
y = df_clean['target']

# ============================================================
# 7. Train/Test Split
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# 8. Scale Features
# ============================================================
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)

# ============================================================
# 9. Train Model
# ============================================================
print("Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = rf_model.predict(X_test_scaled)
print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ============================================================
# 10. Save All Model Assets
# ============================================================
os.makedirs('../models', exist_ok=True)

joblib.dump(rf_model, '../models/habitability_model.pkl')
joblib.dump(scaler, '../models/scaler.pkl')
joblib.dump(num_imputer, '../models/num_imputer.pkl')
joblib.dump(cat_imputer, '../models/cat_imputer.pkl')
joblib.dump(X_train.columns.tolist(), '../models/train_features.pkl')
joblib.dump(star_categories, '../models/star_categories.pkl')

print("\n✅ All model assets saved to ../models/:")
print("  - habitability_model.pkl")
print("  - scaler.pkl")
print("  - num_imputer.pkl")
print("  - cat_imputer.pkl")
print("  - train_features.pkl")
print("  - star_categories.pkl")

# ============================================================
# 11. Quick Sanity Test
# ============================================================
print("\n--- Sanity Test ---")
sample = X_test.iloc[0:1].copy()
sample_scaled = scaler.transform(sample)
prob = rf_model.predict_proba(sample_scaled)[0][1]
print(f"Sample prediction probability: {prob:.4f}")
print(f"Prediction: {'Habitable' if prob > 0.5 else 'Not Habitable'}")
print("✅ Pipeline works correctly!")
