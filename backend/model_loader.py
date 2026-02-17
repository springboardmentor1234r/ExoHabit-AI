import joblib
import os

def load_model():

    # Get project root folder
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Correct absolute path to model
    model_path = os.path.join(BASE_DIR, "models", "habitability_model.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")

    model = joblib.load(model_path)
    return model
