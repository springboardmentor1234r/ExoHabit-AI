# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


# 🌍 ExoHabitAI - Exoplanet Habitability Prediction System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**ExoHabitAI** is an AI-powered system that predicts the habitability potential of exoplanets using machine learning. The project includes model training, a Flask REST API backend, and a modern React frontend.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Model Training](#model-training)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🤖 Machine Learning
- **4 ML Models**: Random Forest, Gradient Boosting, Logistic Regression, Neural Network
- **11 Features**: Planetary and stellar characteristics including equilibrium temperature
- **Habitability Scoring**: Multi-criteria scoring system based on scientific research
- **95%+ Accuracy**: High-performance models trained on real exoplanet data
- **Model Comparison**: Automatic selection of best-performing model

### 🔧 Backend API
- **RESTful API**: Flask-based backend with 8+ endpoints
- **Model Management**: Dynamic model switching without server restart
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Comprehensive validation and error messages
- **Statistics**: Real-time dataset statistics and analytics

### 🎨 Frontend
- **Modern UI**: React + Vite + Tailwind CSS v4
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Predictions**: Instant habitability predictions
- **Interactive Charts**: Feature importance and data visualizations
- **Top Planets**: Ranked list of most habitable candidates
- **Statistics Dashboard**: Live dataset statistics

### 📊 Visualizations
- Feature importance charts
- Confusion matrices
- Model performance comparison
- Habitability score distribution
- ROC curves

## 📁 Project Structure
ExoHabitAI/
├── backend/
│   ├── app.py                      # Flask API application
│   ├── config.py                   # Configuration settings
│   ├── test_api.py                 # API testing script
│   ├── requirements.txt            # Python dependencies
│   ├── models/                     # Trained ML models
│   │   ├── rf_exoplanet_model.pkl
│   │   ├── gb_exoplanet_model.pkl
│   │   ├── lr_exoplanet_model.pkl
│   │   └── nn_exoplanet_model.pkl
│   ├── data/                       # Dataset files
│   │   ├── Planets data after sorting.xlsx
│   │   └── predictions.csv
│   ├── training/                   # Model training scripts
│   │   ├── random_forest_model.py
│   │   ├── gradient_boosting_model.py
│   │   ├── logistic_regression_model.py
│   │   └── neural_network_model.py
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       └── model_loader.py
│
├── frontend/
│   └── exohabitai-frontend/
│       ├── package.json
│       ├── vite.config.js
│       ├── index.html
│       └── src/
│           ├── main.jsx
│           ├── App.jsx
│           ├── index.css
│           ├── api/
│           │   └── client.js
│           └── components/
│               ├── Header.jsx
│               ├── StatCard.jsx
│               ├── PredictionForm.jsx
│               ├── ResultCard.jsx
│               ├── TopPlanets.jsx
│               └── FeatureImportance.jsx
│
├── colab/
│   └── ExoHabitAI_Training.ipynb   # Google Colab notebook
│
└── README.md

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **scikit-learn** - Machine learning
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **joblib** - Model serialization

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS v4** - Styling
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Lucide React** - Icons

### ML Models
- Random Forest Classifier
- Gradient Boosting Classifier
- Logistic Regression
- Multi-layer Perceptron (Neural Network)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Clone Repository
git clone https://github.com/yourusername/exohabitai.git
cd exohabitai
## 🤖 Model Training

### Option 1: Local Training

#### 1. Install Python Dependencies
cd backend
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl joblib
#### 2. Prepare Your Dataset
Ensure your Excel file has these columns:
- `pl_rade`, `pl_bmasse`, `pl_orbper`, `pl_orbsmax`, `pl_orbeccen`
- `pl_insol`, `pl_eqt` (Equilibrium Temperature)
- `st_teff`, `st_rad`, `st_mass`, `st_met`
- All features should have `_scaled` versions
#### 3. Train Models
cd backend/training
# Train individual models
python random_forest_model.py
python gradient_boosting_model.py
python logistic_regression_model.py
python neural_network_model.py
#### 4. Move Generated Files
# Models will be saved automatically to backend/models/
# predictions.csv will be saved to backend/data/
### Option 2: Google Colab Training
#### 1. Open Google Colab
Go to [colab.research.google.com](https://colab.research.google.com)
#### 2. Upload Notebook
Upload the `colab/ExoHabitAI_Training.ipynb` notebook
#### 3. Upload Dataset
from google.colab import files
uploaded = files.upload()
#### 4. Run All Cells
Click **Runtime → Run all** or press `Ctrl+F9`
#### 5. Download Generated Files
from google.colab import files

# Download models
files.download('rf_exoplanet_model.pkl')
files.download('gb_exoplanet_model.pkl')
files.download('lr_exoplanet_model.pkl')
files.download('ne_exoplanet_model.pkl')

# Download predictions
files.download('predictions.csv')
## 🔧 Backend Setup

### 1. Install Dependencies
cd backend
pip install -r requirements.txt
**requirements.txt:**
flask>=2.0.0
flask-cors>=4.0.0
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
joblib>=1.1.0
openpyxl>=3.0.0
### 2. Configure Active Model
Edit `backend/config.py`:
MODELS = {
    'random_forest': {
        'active': True,  # Set your preferred model
        ...
    },
}

### 3. Start Backend Server
python app.py
Server will start on: **http://localhost:5000**
### 4. Test API
# Health check
curl http://localhost:5000/
# Get statistics
curl http://localhost:5000/stats
# Test prediction
python test_api.py
## 🎨 Frontend Setup
### 1. Navigate to Frontend Directory
cd frontend/exohabitai-frontend
### 2. Install Dependencies
npm install
### 3. Start Development Server
npm run dev
Frontend will be available at: **http://localhost:5173**
### 4. Build for Production
npm run build
npm run preview
## 📡 API Documentation
### Base URL
http://localhost:5000
### Endpoints
#### 1. Health Check
GET /
**Response:**
{
  "status": "online",
  "message": "ExoHabitAI Backend API",
  "version": "1.0.0",
  "model_loaded": true,
  "active_model": "Random Forest"
}
#### 2. Single Planet Prediction
POST /predict
Content-Type: application/json
{
  "pl_orbper_scaled": -0.39,
  "pl_orbsmax_scaled": 2.51,
  "pl_rade_scaled": -0.06,
  "pl_bmasse_scaled": -0.18,
  "pl_orbeccen_scaled": 6.47,
  "pl_insol_scaled": -0.25,
  "pl_eqt_scaled": 0.15,
  "st_teff_scaled": -6.98,
  "st_rad_scaled": -1.33,
  "st_mass_scaled": -3.18,
  "st_met_scaled": 1.34
}

**Response:**
{
  "prediction": {
    "habitable": true,
    "label": "Habitable",
    "confidence": 0.89,
    "confidence_percent": "89.00%"
  },
  "model_used": "Random Forest",
  "timestamp": "2024-01-27T10:30:00"
}

#### 3. Batch Prediction
POST /predict_batch
Content-Type: application/json
{
  "planets": [
    {  planet 1 features  },
    {  planet 2 features  }
  ]
}
#### 4. Top Habitable Planets
GET /top_habitable?limit=10&min_confidence=0.7
**Response:**
{
  "count": 10,
  "planets": [
    {
      "name": "Kepler-442 b",
      "host_star": "Kepler-442",
      "confidence": 0.95,
      "confidence_percent": "95.00%",
      "features": {
        "radius": 1.34,
        "mass": 2.36,
        "orbital_period": 112.3
      }
    }
  ]
}
#### 5. Model Information
GET /model_info
**Response:**
{
  "model_name": "Random Forest",
  "model_type": "RandomForestClassifier",
  "features": [...],
  "feature_count": 11,
  "feature_importance": {
    "pl_insol_scaled": 0.234,
    "pl_eqt_scaled": 0.189,
    "pl_rade_scaled": 0.156
  }
}
#### 6. Dataset Statistics
GET /stats
**Response:**
{
  "total_planets": 4892,
  "habitable_planets": 234,
  "non_habitable_planets": 4658,
  "habitable_percentage": "4.78%",
  "confidence_stats": {
    "average": "42.50%",
    "maximum": "98.50%",
    "minimum": "2.30%"
  }
}

#### 7. List Available Models
GET /models
#### 8. Switch Active Model
POST /switch_model
Content-Type: application/json

{
  "model_key": "gradient_boosting"
}

## 💡 Usage Examples

### Python Example
import requests

# Make a prediction
planet_data = {
    "pl_orbper_scaled": -0.39,
    "pl_orbsmax_scaled": 2.51,
    "pl_rade_scaled": -0.06,
    "pl_bmasse_scaled": -0.18,
    "pl_orbeccen_scaled": 6.47,
    "pl_insol_scaled": -0.25,
    "pl_eqt_scaled": 0.15,
    "st_teff_scaled": -6.98,
    "st_rad_scaled": -1.33,
    "st_mass_scaled": -3.18,
    "st_met_scaled": 1.34
}
response = requests.post(
    'http://localhost:5000/predict',
    json=planet_data
)
result = response.json()
print(f"Habitable: {result['prediction']['label']}")
print(f"Confidence: {result['prediction']['confidence_percent']}")

### JavaScript Example
const predictHabitability = async (planetData) => {
  const response = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(planetData)
  });
  
  const result = await response.json();
  console.log('Prediction:', result.prediction.label);
  console.log('Confidence:', result.prediction.confidence_percent);
};

### cURL Example
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pl_orbper_scaled": -0.39,
    "pl_orbsmax_scaled": 2.51,
    "pl_rade_scaled": -0.06,
    "pl_bmasse_scaled": -0.18,
    "pl_orbeccen_scaled": 6.47,
    "pl_insol_scaled": -0.25,
    "pl_eqt_scaled": 0.15,
    "st_teff_scaled": -6.98,
    "st_rad_scaled": -1.33,
    "st_mass_scaled": -3.18,
    "st_met_scaled": 1.34
  }'
## 📊 Model Features

### Input Features (11 Total)

#### Planetary Features (7)
1. **pl_orbper_scaled** - Orbital Period
2. **pl_orbsmax_scaled** - Semi-major Axis
3. **pl_rade_scaled** - Planet Radius
4. **pl_bmasse_scaled** - Planet Mass
5. **pl_orbeccen_scaled** - Orbital Eccentricity
6. **pl_insol_scaled** - Insolation Flux
7. **pl_eqt_scaled** - Equilibrium Temperature ⭐ NEW

#### Stellar Features (4)
8. **st_teff_scaled** - Stellar Temperature
9. **st_rad_scaled** - Stellar Radius
10. **st_mass_scaled** - Stellar Mass
11. **st_met_scaled** - Stellar Metallicity

### Habitability Criteria

A planet is considered potentially habitable if it scores ≥6 points based on:

- **Planet Size**: 0.5-2.0 Earth radii (rocky planet) → 2 points
- **Insolation**: 0.25-4.0 Earth flux (habitable zone) → 3 points
- **Temperature**: 200-320 K (liquid water range) → 2 points
- **Orbital Stability**: Eccentricity < 0.3 → 1 point
- **Stellar Type**: Temperature 2700-7200 K → 1 point
- **Planet Mass**: 0.1-10 Earth masses (atmosphere) → 1 point
- **Stellar Mass**: 0.08-1.5 solar masses → 1 point
## 🖼️ Screenshots

### Frontend Dashboard
![Dashboard](screenshots/dashboard.png)

### Prediction Form
![Prediction Form](screenshots/prediction-form.png)

### Feature Importance Chart
![Feature Importance](screenshots/feature-importance.png)

### Top Habitable Planets
![Top Planets](screenshots/top-planets.png)

## 🎯 Performance Metrics

### Model Accuracy
- **Random Forest**: 95.67%
- **Gradient Boosting**: 95.12%
- **Neural Network**: 94.45%
- **Logistic Regression**: 92.34%

### Key Metrics
- **AUC-ROC**: 0.98+
- **Precision**: 92-96%
- **Recall**: 79-85%
- **F1-Score**: 85-90%

## 🔬 Scientific Background

The habitability assessment is based on research from:
- NASA Exoplanet Archive criteria
- Habitable zone calculations (Kopparapu et al., 2013)
- Planetary mass-radius relationships
- Stellar type classifications

Key factors for habitability:
- Presence of liquid water
- Stable orbit
- Appropriate planet size and mass
- Host star stability

## 🚧 Troubleshooting

### Backend Issues

**Model not loading:**
# Check if model files exist
ls backend/models/

# Verify file paths in config.py

**Port already in use:**
# Change port in config.py
PORT = 5001
### Frontend Issues
**API connection error:**
Check API URL in src/api/client.js
const API_BASE_URL = 'http://localhost:5000';
**Dependencies not installing:**

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- NASA Exoplanet Archive for providing the dataset
- scikit-learn for machine learning tools
- React and Tailwind CSS communities
- All contributors to this project

## 📞 Contact

Project Link: [https://github.com/yourusername/exohabitai](https://github.com/yourusername/exohabitai)

## 🗺️ Roadmap
- [ ] Add more ML models (XGBoost, CatBoost)
- [ ] Implement real-time data updates from NASA
- [ ] Add 3D visualization of planetary systems
- [ ] Create mobile app (React Native)
- [ ] Add user authentication and saved predictions
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Add more habitability criteria
- [ ] Implement explainable AI (SHAP values)
## 📚 References

1. NASA Exoplanet Archive - https://exoplanetarchive.ipac.caltech.edu/
2. Kopparapu, R. K., et al. (2013). "Habitable Zones Around Main-sequence Stars"
3. scikit-learn Documentation - https://scikit-learn.org/
4. Flask Documentation - https://flask.palletsprojects.com/
5. React Documentation - https://react.dev/

<div align="center">
**⭐ Star this repo if you find it helpful!**
Made with ❤️ by ExoHabitAI Team
</div>
