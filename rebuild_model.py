import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

# Load data
df = pd.read_csv("data/exoplanet_clean_40k.csv")

# Select features
df = df[[
    'pl_rade',      # planet radius
    'pl_bmasse',    # planet mass
    'pl_orbper',    # orbital period
    'pl_eqt',       # equilibrium temp
    'st_teff',      # star temperature
    'st_lum'        # star luminosity
]]

# Clean data
df = df.dropna()
df = df[df['pl_eqt'] < 1000]  # remove extreme outliers

# Create target variable
df['habitable'] = ((df['pl_eqt'] >= 273.15) & (df['pl_eqt'] <= 373.15)).astype(int)

# Prepare features and labels
X = df.drop("habitable", axis=1)
y = df["habitable"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train RandomForest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate model
print("Random Forest Model Report:")
print(classification_report(y_test, model.predict(X_test)))
try:
    print("ROC AUC:", roc_auc_score(y_test, model.predict_proba(X_test)[:,1]))
except:
    print("ROC AUC: Cannot compute (only one class in test set)")

# Save model and scaler
joblib.dump(model, "model/habitability_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("\nModel and scaler saved successfully!")
