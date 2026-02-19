import joblib
import pandas as pd
import numpy as np

class HabitabilityModel:
    def __init__(self):
        self.model = joblib.load("models/xgboost_model.pkl")
        self.scaler = joblib.load("models/scaler.pkl")
        self.features = joblib.load("models/feature_order.pkl")

    def predict(self, payload):
        df = pd.DataFrame([payload])[self.features]
        X = self.scaler.transform(df)
        probs = self.model.predict_proba(X)[0]

        return probs.tolist()
