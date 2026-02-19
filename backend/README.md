# Exoplanet Habitability Predictor

A full-stack ML application that predicts exoplanet habitability using a Random Forest classifier trained on NASA exoplanet data.

## Project Structure

```
python-backend/
├── app.py                    # Flask API server
├── export_model.py           # Script to train & export model assets
├── precompute_rankings.py    # Script to precompute rankings & dashboard data
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment config for Render/Heroku
├── models/                   # Generated model assets (after running export_model.py)
│   ├── habitability_model.pkl
│   ├── scaler.pkl
│   ├── num_imputer.pkl
│   ├── cat_imputer.pkl
│   ├── train_features.pkl
│   ├── star_categories.pkl
│   ├── rankings.csv
│   └── dashboard_data.json
└── templates/                # HTML templates (optional, API-first)
```

## Setup Instructions

### 1. Install Dependencies
```bash
cd python-backend
pip install -r requirements.txt
```

### 2. Prepare Data
Place your `Exoplanet_habitability_dataset.csv` file in the `python-backend/` directory.

### 3. Train & Export Model
```bash
python export_model.py
```
This will create the `models/` directory with all fitted preprocessors and the trained model.

### 4. Precompute Rankings & Dashboard Data
```bash
python precompute_rankings.py
```

### 5. Run the Flask App
```bash
python app.py
```
The API will be available at `http://localhost:5000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Predict habitability for a single exoplanet |
| GET | `/rankings?top=20` | Get top ranked candidates |
| GET | `/features` | Get expected input features |
| GET | `/feature-importance` | Get model feature importance |
| GET | `/dashboard-data` | Get aggregated dashboard data |

### Example: POST /predict
```json
{
  "pl_orbper": 365.25,
  "pl_orbsmax": 1.0,
  "pl_rade": 1.0,
  "pl_masse": 1.0,
  "pl_dens": 5.51,
  "pl_insol": 1.0,
  "pl_eqt": 255,
  "st_teff": 5778,
  "st_met": 0.0,
  "st_lum": 0.0,
  "st_spectype": "G"
}
```

### Response
```json
{
  "prediction": "Potentially Habitable",
  "probability": 0.87,
  "habitability_score": 0.92,
  "stellar_compatibility": 0.95,
  "class": 1
}
```

## Deployment on Render (Free Tier)

1. Push the `python-backend/` directory to a GitHub repo
2. Create a new **Web Service** on [Render](https://render.com)
3. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Deploy!

## Connecting the React Frontend

Update the API base URL in the React app to point to your deployed Flask backend. The frontend uses mock data by default and can be switched to live API calls.

## Model Details

- **Algorithm**: Random Forest Classifier (100 trees, random_state=42)
- **Features**: 10 numerical + 1 categorical (star spectral type)
- **Engineered Features**: Habitability Score (Earth Similarity Index), Stellar Compatibility Index
- **Target**: Binary (habitability_score > 0.5)
- **Dataset**: ~39,212 exoplanets from NASA Exoplanet Archive
