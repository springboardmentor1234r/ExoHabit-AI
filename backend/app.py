"""
Flask API for Exoplanet Habitability Prediction
===============================================
Exposes a trained Random Forest ML model through REST APIs.
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import os
import random # Added for Random Sample feature

# Get the project root directory (parent of backend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

# Get the directory where this script is located
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
SCALER_PATH = os.path.join(BACKEND_DIR, "scaler.joblib")

# Model Paths
MODEL_PATHS = {
    'rf': os.path.join(BACKEND_DIR, "Random_Forest_model.joblib"),
    'xgb': os.path.join(BACKEND_DIR, "XGBoost_model.joblib"),
    'lr': os.path.join(BACKEND_DIR, "Logistic_Regression_model.joblib")
}

REQUIRED_FEATURES = [
    'pl_orbper',    # Orbital period (days)
    'pl_rade',      # Planet radius (Earth radii)
    'pl_bmasse',    # Planet mass (Earth masses)
    'pl_eqt',       # Equilibrium temperature (K)
    'st_teff',      # Stellar effective temperature (K)
    'st_rad',       # Stellar radius (Solar radii)
    'st_mass',      # Stellar mass (Solar masses)
    'sy_dist',      # Distance to system (parsec)
    'sy_snum',      # Number of stars in system
    'sy_pnum'       # Number of planets in system
]

# Global variables to store loaded models
loaded_models = {}
scaler = None


def load_model():
    """Load the trained models and scaler."""
    global loaded_models, scaler
    
    # Load Scaler
    if os.path.exists(SCALER_PATH):
        try:
            scaler = joblib.load(SCALER_PATH)
            print(f"✓ Scaler loaded from {SCALER_PATH}")
        except Exception as e:
            print(f"✗ Error loading scaler: {e}")
            return False
    else:
        print(f"✗ Scaler file not found: {SCALER_PATH}")
        return False

    # Load Models
    success_count = 0
    for key, path in MODEL_PATHS.items():
        if os.path.exists(path):
            try:
                loaded_models[key] = joblib.load(path)
                print(f"✓ Model '{key}' loaded from {path}")
                success_count += 1
            except Exception as e:
                print(f"✗ Error loading model '{key}': {e}")
        else:
            print(f"⚠ Model file not found for '{key}': {path}")

    return success_count > 0


def validate_input(data):
    """
    Validate input data for prediction.
    Returns (is_valid, error_message, validated_data)
    """
    if not isinstance(data, dict):
        return False, "Input must be a JSON object", None
    
    missing_features = []
    for feature in REQUIRED_FEATURES:
        if feature not in data:
            missing_features.append(feature)
    
    if missing_features:
        return False, f"Missing required features: {', '.join(missing_features)}", None
    
    validated_data = {}
    invalid_features = []
    
    for feature in REQUIRED_FEATURES:
        value = data[feature]
        # Allow string numbers convertible to float
        try:
            float_val = float(value)
            validated_data[feature] = float_val
            if np.isnan(float_val) or np.isinf(float_val):
                invalid_features.append(f"{feature} (invalid value)")
        except (ValueError, TypeError):
             invalid_features.append(f"{feature} (must be numeric)")
    
    if invalid_features:
        return False, f"Invalid values for: {', '.join(invalid_features)}", None
    
    return True, None, validated_data


def get_feature_importance(model, model_type):
    """Extract feature importance from model."""
    try:
        if model_type == 'rf' or model_type == 'xgb':
            if hasattr(model, 'feature_importances_'):
                raw_importance = model.feature_importances_
            else:
                return {}
        elif model_type == 'lr':
            if hasattr(model, 'coef_'):
                # Use absolute value of coefficients
                raw_importance = np.abs(model.coef_[0])
            else:
                return {}
        else:
            return {}

        # Normalize
        total = np.sum(raw_importance)
        if total > 0:
            normalized = raw_importance / total
            return {feat: float(score) for feat, score in zip(REQUIRED_FEATURES, normalized)}
    except:
        pass
    return {}


def make_prediction(data, model_type='rf'):
    """
    Make habitability prediction using the loaded model.
    Returns prediction result dictionary.
    """
    try:
        model = loaded_models.get(model_type)
        if not model:
            return {"success": False, "error": f"Model '{model_type}' not available"}

        feature_values = [data[feature] for feature in REQUIRED_FEATURES]
        features_array = np.array(feature_values).reshape(1, -1)
        
        features_scaled = scaler.transform(features_array)
        
        prediction = model.predict(features_scaled)[0]
        # Check if model supports predict_proba
        try:
            if hasattr(model, 'predict_proba'):
                probability = model.predict_proba(features_scaled)[0][1]
            else:
                probability = float(prediction)
            
            habitability_probability = float(probability)
        except:
             habitability_probability = float(prediction)

        is_habitable = int(prediction)
        
        confidence = "High" if habitability_probability > 0.8 or habitability_probability < 0.2 else "Medium"
        
        feature_contributions = get_feature_importance(model, model_type)

        return {
            "success": True,
            "prediction": {
                "is_habitable": is_habitable,
                "habitability_probability": round(habitability_probability, 4),
                "confidence": confidence,
                "model_used": model_type.upper(),
                "classification": "Habitable" if is_habitable == 1 else "Not Habitable"
            },
            "feature_importance": feature_contributions,
            "input_data": data
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Prediction failed: {str(e)}"
        }


# ===== WEBSITE ROUTES =====

@app.route('/', methods=['GET'])
def index_website():
    """Serve the main website."""
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({
            "error": f"Template error: {str(e)}",
            "template_folder": app.template_folder,
            "static_folder": app.static_folder
        }), 500


@app.route('/famous', methods=['GET'])
def famous_planets():
    """Serve the famous planets page."""
    return render_template('famous.html')

@app.route('/learn', methods=['GET'])
def learn_page():
    return render_template('learn.html')

@app.route('/candidates', methods=['GET'])
def candidates_page():
    return render_template('candidates.html')

@app.route('/visualize', methods=['GET'])
def visualize_page():
    return render_template('visualize.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(STATIC_DIR, filename)


# ===== API ROUTES =====

@app.route('/api', methods=['GET'])
def index_api():
    """Root endpoint with API information."""
    return jsonify({
        "message": "Exoplanet Habitability Prediction API",
        "version": "2.0.0",
        "models_available": list(loaded_models.keys()),
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "random_planet": "/random-planet"
        },
        "model_loaded": len(loaded_models) > 0 and scaler is not None
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy" if loaded_models and scaler is not None else "degraded",
        "models_loaded": list(loaded_models.keys()),
        "scaler_loaded": scaler is not None
    })


@app.route('/features', methods=['GET'])
def features():
    """Get list of required features."""
    descriptions = {
        'pl_orbper': 'Orbital period (days)',
        'pl_rade': 'Planet radius (Earth radii)',
        'pl_bmasse': 'Planet mass (Earth masses)',
        'pl_eqt': 'Equilibrium temperature (K)',
        'st_teff': 'Stellar effective temperature (K)',
        'st_rad': 'Stellar radius (Solar radii)',
        'st_mass': 'Stellar mass (Solar masses)',
        'sy_dist': 'Distance to system (parsec)',
        'sy_snum': 'Number of stars in system',
        'sy_pnum': 'Number of planets in system'
    }
    return jsonify({
        "required_features": REQUIRED_FEATURES,
        "descriptions": descriptions
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict habitability.
    JSON Body: { ...planet_data..., "model_type": "rf"|"xgb"|"lr" }
    """
    if not loaded_models or not scaler:
        return jsonify({"success": False, "error": "System initializing or models failed to load."}), 503
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
        
        # Extract model type (default to Random Forest)
        model_type = data.pop('model_type', 'rf').lower()
        if model_type not in loaded_models:
            model_type = 'rf' # Fallback
            
        is_valid, error_msg, validated_data = validate_input(data)
        if not is_valid:
            return jsonify({"success": False, "error": error_msg}), 400
        
        result = make_prediction(validated_data, model_type)
        status_code = 200 if result["success"] else 500
        return jsonify(result), status_code
            
    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route('/random-planet', methods=['GET'])
def random_planet():
    """Generate a random planet for testing."""
    planet = {
        'pl_orbper': round(random.uniform(10, 500), 2),
        'pl_rade': round(random.uniform(0.5, 2.5), 2),
        'pl_bmasse': round(random.uniform(0.1, 10.0), 2),
        'pl_eqt': round(random.uniform(200, 400), 1),
        'st_teff': round(random.uniform(3000, 7000), 0),
        'st_rad': round(random.uniform(0.1, 2.0), 2),
        'st_mass': round(random.uniform(0.1, 2.0), 2),
        'sy_dist': round(random.uniform(5, 100), 1),
        'sy_snum': random.randint(1, 3),
        'sy_pnum': random.randint(1, 8)
    }
    return jsonify({"success": True, "planet": planet})


# Initialize resources on startup
print("=" * 60)
print("PlanetAI System Initialization")
print("=" * 60)
if load_model():
    print("✓ System ready.")
    print(f"Loaded models: {list(loaded_models.keys())}")
else:
    print("✗ System initialization failed.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
   