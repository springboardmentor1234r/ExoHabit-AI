from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from exohabitai.data.feature_engineering import feature_engineering

from flask_sqlalchemy import SQLAlchemy
from backend.database import db, init_db, Planet

# ... imports ...

app = Flask(__name__, 
            template_folder='../frontend',
            static_folder='../static')

# Initialize DB
init_db(app)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../exohabitai/models/habitability_model.pkl')
model = None

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/exoplanets')
def exoplanets():
    return render_template('exoplanets.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        input_df = feature_engineering(input_df)
        
        expected_features = [
            'pl_rade', 'pl_masse', 'pl_orbper', 'pl_eqt', 'pl_dens', 
            'st_teff', 'st_rad', 'st_mass', 'sy_dist'
        ]
        
        missing = [col for col in expected_features if col not in input_df.columns]
        if missing:
             for col in missing:
                 input_df[col] = 0
        
        X_pred = input_df[expected_features]
        
        prediction = model.predict(X_pred)[0]
        probability = model.predict_proba(X_pred)[0][1]
        
        result = {
            'prediction': int(prediction),
            'probability': float(probability),
            'habitable': bool(prediction == 1)
        }
        
        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Prediction Error: {e}")
        return jsonify({'error': str(e)}), 400 

@app.route('/data')
def data():
    """
    Return stats and top candidates from Database.
    """
    try:
        # Get stats
        total_planets = Planet.query.count()
        habitable_count = Planet.query.filter_by(is_habitable=True).count()
        
        # Get top 10 candidates
        candidates = Planet.query.filter_by(is_habitable=True)\
                                 .order_by(Planet.habitability_score.desc())\
                                 .limit(10).all()
        
        candidates_list = []
        for i, p in enumerate(candidates):
            candidates_list.append({
                'rank': i+1,
                'name': p.pl_name,
                'score': round(p.habitability_score * 100, 1), # Assuming score is 0-1
                'dist': round(p.sy_dist, 1) if p.sy_dist else 0,
                'status': 'Habitable'
            })
            
        return jsonify({
            'total_planets': total_planets,
            'habitable_candidates': habitable_count,
            'candidates': candidates_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
