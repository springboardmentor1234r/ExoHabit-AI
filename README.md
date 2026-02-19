# ExoHabitAI — Exoplanet Habitability Predictor

A full-stack machine learning application that predicts exoplanet habitability using a Random Forest classifier trained on NASA Exoplanet Archive data. The system includes an interactive web dashboard for exploring predictions, rankings, and model insights.

## Project Structure

```
ExoHabitAI/
├── backend/            # Flask REST API and ML pipeline scripts
├── dashboard/          # Dashboard-specific views and configuration
├── data/
│   ├── raw/            # Original unprocessed datasets
│   └── processed/      # Cleaned and feature-engineered datasets
├── deployment/         # Hosting configuration (Procfile, platform configs)
├── frontend/           # Frontend documentation (source in src/)
├── models/             # Trained model artifacts (.pkl files)
├── notebooks/          # Jupyter notebooks for EDA and model development
├── src/                # React frontend source code
├── public/             # Static frontend assets
└── requirements.txt    # Python dependencies (root-level reference)
```

## Installation

### Prerequisites

- Node.js >= 18
- Python >= 3.9

### Frontend Setup

```bash
npm install
npm run dev
```

The development server starts at `http://localhost:8080`.

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

#### Prepare Model Assets

1. Place `Exoplanet_habitability_dataset.csv` in the `data/raw/` directory.
2. Train the model and export artifacts:

```bash
python export_model.py
```

3. Precompute rankings and dashboard data:

```bash
python precompute_rankings.py
```

4. Start the API server:

```bash
python app.py
```

The API runs at `http://localhost:5000`.

## Usage

### Prediction

Submit exoplanet parameters (orbital period, radius, equilibrium temperature, stellar type, etc.) through the web form or via the `/predict` endpoint to receive a habitability probability score.

### Rankings

Browse the top exoplanet candidates ranked by habitability probability, with filtering and sorting capabilities.

### Dashboard

Explore interactive visualizations including:
- Habitability score distribution
- Feature importance from the Random Forest model
- Stellar type breakdown across the dataset

## API Endpoints

| Method | Endpoint              | Description                          |
|--------|-----------------------|--------------------------------------|
| POST   | `/predict`            | Predict habitability for one planet  |
| GET    | `/rankings?top=N`     | Top N habitable candidates           |
| GET    | `/features`           | List of expected input features      |
| GET    | `/feature-importance` | Model feature importance scores      |
| GET    | `/dashboard-data`     | Aggregated dashboard statistics      |

## Tech Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts
- **Backend**: Python, Flask, scikit-learn, pandas
- **ML Model**: Random Forest Classifier (100 estimators)
- **Deployment**: Gunicorn, static hosting for frontend

## License

This project was developed as part of an academic research initiative on exoplanet habitability prediction.
