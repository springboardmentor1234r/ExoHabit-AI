import pandas as pd
import numpy as np
import os
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# ==============================
# Load Dataset
# ==============================
df = pd.read_csv("processed_exoplanets.csv")

# ==============================
# Feature Columns
# ==============================
feature_columns = [
    "pl_orbper",
    "pl_orbsmax",
    "pl_bmasse",
    "pl_eqt",
    "st_teff",
    "st_rad",
    "st_mass",
    "st_lum",
    "pl_rade",
    "pl_insol"
]

X = df[feature_columns]
y = df["habitability_label"]

# ==============================
# Train-Test Split
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# Model
# ==============================
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ==============================
# Predictions
# ==============================
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# ==============================
# Evaluation Metrics
# ==============================
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc = roc_auc_score(y_test, y_prob)

cm = confusion_matrix(y_test, y_pred)

print("\nModel Performance:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("ROC-AUC:", roc)
print("Confusion Matrix:\n", cm)

# ==============================
# Save Model
# ==============================
model_path = os.path.join("..", "models", "habitability_model.pkl")
joblib.dump(model, model_path)

print("\nModel retrained and saved successfully.")

# ==============================
# Save Metrics for Dashboard
# ==============================
metrics = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1_score": float(f1),
    "roc_auc": float(roc),
    "true_negative": int(cm[0][0]),
    "false_positive": int(cm[0][1]),
    "false_negative": int(cm[1][0]),
    "true_positive": int(cm[1][1]),
    "total_samples": int(len(df))
}

metrics_path = os.path.join("..", "models", "model_metrics.json")

with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=4)

print("Metrics saved successfully.")
