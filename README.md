# Exoplanet Habitability Prediction System

A full-stack machine learning web application that predicts the habitability potential of exoplanets using planetary and stellar characteristics. The system integrates a trained Random Forest model with a Flask backend and an interactive frontend dashboard.

---

## Project Overview

This project analyzes real NASA exoplanet data and predicts whether a planet is potentially habitable. It demonstrates a complete end-to-end machine learning pipeline, including:

- Data preprocessing and feature engineering
- Model training and evaluation
- Backend API development
- Frontend interface with visualization dashboard
- Export functionality (PDF and CSV)

The model was trained on 40,000+ exoplanet observations.

---

## Key Features

### Machine Learning Model
- Algorithm: RandomForestClassifier
- Estimators: 100 decision trees
- Accuracy: ~94% on test dataset
- Binary classification (Habitable / Non-Habitable)
- Feature importance analysis included

### Habitability Scoring System
The final habitability score (0–100 scale) is calculated using:
- Model prediction probability
- Temperature proximity to habitable range (273K–373K)

The score is categorized into four tiers:
- 80–100: Highly Habitable
- 60–79: Likely Habitable
- 40–59: Possibly Habitable
- 0–39: Low Habitability

### Web Application
- Flask-based REST API
- Bootstrap responsive UI
- Interactive dashboard using Chart.js
- PDF and CSV export functionality

---

## Input Features

The model uses six planetary and stellar parameters:

1. Planet Radius (Earth radii)
2. Planet Mass (Earth masses)
3. Orbital Period (days)
4. Equilibrium Temperature (Kelvin)
5. Star Temperature (Kelvin)
6. Star Luminosity (Solar units)

---

## Technology Stack

### Backend
- Python 3.8+
- Flask
- scikit-learn
- joblib
- pandas
- numpy
- reportlab (PDF generation)

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Chart.js
- JavaScript (ES6)

---

## Project Structure

Exoplanet-Habitability/
├── backend/
│ ├── app.py
│ ├── requirements.txt
│ ├── templates/
│ │ ├── index.html
│ │ └── dashboard.html
│
├── model/
│ ├── habitability_model.pkl
│ └── scaler.pkl
│
├── notebook/
│ └── exoplanet_habitability.ipynb
│
├── data/
│ └── exoplanet_clean_40k.csv
│
├── README.md
└── PROJECT_DOCUMENTATION.md


---

## How to Run the Project

1. Navigate to the backend folder:

2. Install dependencies:

3. Run the Flask server:

4. Open in browser:
- Prediction Page: http://127.0.0.1:5000
- Dashboard: http://127.0.0.1:5000/dashboard

---

## 📦 Containerized Deployment (Docker)

Recommended for portability and easy local or cloud deployment. The repository includes a `Dockerfile` and `docker-compose.yml` to run the Flask app in a container.

Prerequisites:
- Docker installed
- (Optional) docker-compose installed
- Ensure `model/habitability_model.pkl` and `model/scaler.pkl` exist in the `model/` folder

Build and run with Docker:

```bash
# from project root
docker build -t exoplanet-habitability:latest .
docker run --rm -p 5000:5000 -v $(pwd)/model:/app/model:ro -v $(pwd)/data:/app/data:ro exoplanet-habitability:latest
```

Using docker-compose (recommended for local dev):

```bash
docker-compose up --build
```

The service will be available at `http://127.0.0.1:5000`.

Notes:
- The `docker-compose.yml` mounts `./model` and `./data` into the container as read-only volumes so you can iterate on model/data without rebuilding the image.
- The container runs Gunicorn as the WSGI server for better production behavior than Flask's built-in server.

---

## 🚀 Deploy to Render (fast, hosted URL)

Render can build this repository directly (it supports Docker deployments). Steps:

1. Push this repository to GitHub (or your git host).
2. Go to https://dashboard.render.com and create a new Web Service.
3. Connect your GitHub repo and select the `main` branch (or the branch you pushed).
4. For **Environment**, choose `Docker` so Render will use the repository `Dockerfile`.
5. Leave the build and start commands empty (the Dockerfile runs Gunicorn). Set the plan to `Free` if you want a free instance.
6. Add any environment variables if needed (Render provides `PORT` automatically).

Render will build the container and give you a public HTTPS URL (e.g., `https://your-service.onrender.com`).

Recommended: add `render.yaml` (included) to the repo so you can recreate the service via Render's spec import.

Healthcheck: the app exposes `/health` which returns `{"status":"ok"}` when ready; configure Render's health check to use that path.


---

## API Endpoints

### GET `/`
Returns the prediction interface.

### POST `/predict`
Accepts six input parameters and returns:
- Habitability score (0–100)
- Model confidence
- Classification tier

### GET `/dashboard`
Displays analytics and visualizations.

---

## Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | ~94% |
| Training Records | 40,000+ |
| Test Size | ~8,000 |
| Algorithm | RandomForestClassifier |
| Estimators | 100 |

---

## System Workflow

User Input
↓
Flask Backend
↓
Feature Scaling
↓
Random Forest Model
↓
Habitability Score Calculation
↓
Result Display & Dashboard Visualization

---

## Conclusion

This project demonstrates a production-style machine learning system integrating data processing, model development, API design, frontend engineering, and visualization into a unified application for exoplanet habitability analysis.

---

## License

NASA exoplanet dataset used for educational purposes.
