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

# Get the project root directory (parent of backend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

MODEL_PATH = "Random_Forest_model.joblib"
SCALER_PATH = "scaler.joblib"

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

model = None
scaler = None


def load_model():
    """Load the trained model and scaler."""
    global model, scaler
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print(f"✓ Model loaded from {MODEL_PATH}")
        else:
            print(f"✗ Model file not found: {MODEL_PATH}")
            return False
        
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            print(f"✓ Scaler loaded from {SCALER_PATH}")
        else:
            print(f"✗ Scaler file not found: {SCALER_PATH}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error loading model: {str(e)}")
        return False


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
        if not isinstance(value, (int, float)):
            invalid_features.append(f"{feature} (must be numeric)")
        elif np.isnan(value) or np.isinf(value):
            invalid_features.append(f"{feature} (invalid value)")
        else:
            validated_data[feature] = float(value)
    
    if invalid_features:
        return False, f"Invalid values for: {', '.join(invalid_features)}", None
    
    return True, None, validated_data


def make_prediction(data):
    """
    Make habitability prediction using the loaded model.
    Returns prediction result dictionary.
    """
    try:
        feature_values = [data[feature] for feature in REQUIRED_FEATURES]
        features_array = np.array(feature_values).reshape(1, -1)
        
        features_scaled = scaler.transform(features_array)
        
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]
        
        habitability_probability = float(probability[1])
        is_habitable = int(prediction)
        
        confidence = "High" if habitability_probability > 0.8 or habitability_probability < 0.2 else "Medium"
        
        return {
            "success": True,
            "prediction": {
                "is_habitable": is_habitable,
                "habitability_probability": round(habitability_probability, 4),
                "confidence": confidence,
                "classification": "Habitable" if is_habitable == 1 else "Not Habitable"
            },
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


@app.route('/test', methods=['GET'])
def test_page():
    """Test route to verify server is working."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body style="background: #0a0a0a; color: white; font-family: Arial; padding: 50px;">
        <h1>✓ Flask Server is Running!</h1>
        <p>Now try accessing <a href="/" style="color: #00d4ff;">the main website</a></p>
        <p>Template folder: {}</p>
        <p>Static folder: {}</p>
        <p><a href="/test-sections" style="color: #00d4ff;">View Section Test Page</a></p>
    </body>
    </html>
    """.format(app.template_folder, app.static_folder)


@app.route('/test-sections', methods=['GET'])
def test_sections():
    """Test page showing all sections."""
    return render_template('test_sections.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory(STATIC_DIR, filename)


# ===== API ROUTES =====

@app.route('/api', methods=['GET'])
def index():
    """Root endpoint with API information."""
    return jsonify({
        "message": "Exoplanet Habitability Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "features": "/features"
        },
        "model_loaded": model is not None and scaler is not None
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy" if model is not None and scaler is not None else "unhealthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    })


@app.route('/features', methods=['GET'])
def features():
    """Get list of required features for prediction."""
    feature_descriptions = {
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
        "feature_descriptions": feature_descriptions,
        "count": len(REQUIRED_FEATURES)
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict habitability of an exoplanet.
    
    Expected JSON input:
    {
        "pl_orbper": float,
        "pl_rade": float,
        "pl_bmasse": float,
        "pl_eqt": float,
        "st_teff": float,
        "st_rad": float,
        "st_mass": float,
        "sy_dist": float,
        "sy_snum": int,
        "sy_pnum": int
    }
    """
    if model is None or scaler is None:
        return jsonify({
            "success": False,
            "error": "Model not loaded. Please check server configuration."
        }), 503
    
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        is_valid, error_message, validated_data = validate_input(data)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message
            }), 400
        
        result = make_prediction(validated_data)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint for multiple exoplanets.
    
    Expected JSON input:
    {
        "planets": [
            {"pl_orbper": 365.25, "pl_rade": 1.0, ...},
            {"pl_orbper": 100.0, "pl_rade": 2.5, ...}
        ]
    }
    """
    if model is None or scaler is None:
        return jsonify({
            "success": False,
            "error": "Model not loaded. Please check server configuration."
        }), 503
    
    try:
        data = request.get_json()
        
        if data is None or 'planets' not in data:
            return jsonify({
                "success": False,
                "error": "Invalid input. Expected {'planets': [...]}"
            }), 400
        
        planets = data['planets']
        
        if not isinstance(planets, list):
            return jsonify({
                "success": False,
                "error": "'planets' must be a list"
            }), 400
        
        if len(planets) > 100:
            return jsonify({
                "success": False,
                "error": "Batch size limit exceeded. Maximum 100 planets per request."
            }), 400
        
        results = []
        errors = []
        
        for i, planet in enumerate(planets):
            is_valid, error_message, validated_data = validate_input(planet)
            
            if not is_valid:
                errors.append({
                    "index": i,
                    "error": error_message,
                    "input": planet
                })
            else:
                prediction = make_prediction(validated_data)
                results.append({
                    "index": i,
                    **prediction
                })
        
        return jsonify({
            "success": True,
            "batch_results": results,
            "errors": errors,
            "total_processed": len(planets),
            "successful": len(results),
            "failed": len(errors)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found. Visit / for API documentation."
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Exoplanet Habitability Prediction API")
    print("=" * 60)
    
    if load_model():
        print("\n✓ API ready to serve predictions!")
        print("\nAvailable endpoints:")
        print("  GET  /          - API information")
        print("  GET  /health    - Health check")
        print("  GET  /features  - List required features")
        print("  POST /predict   - Single prediction")
        print("  POST /batch-predict - Batch predictions")
        print("\n" + "=" * 60)
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("\n✗ Failed to load model. Please ensure model files exist.")
        print("\nExpected files:")
        print(f"  - {MODEL_PATH}")
        print(f"  - {SCALER_PATH}")
        exit(1)
