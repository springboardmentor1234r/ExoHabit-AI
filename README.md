# ExoHabit-AI 🪐

ExoHabit-AI is a machine learning-powered application that predicts the potential habitability of exoplanets based on their physical and stellar parameters.

## 🚀 Features
- **Habitability Prediction**: Uses Random Forest / XGBoost to classify planets.
- **Interactive Dashboard**: Visualizes exoplanetary data.
- **REST API**: Flask backend serving predictions.
- **Modern UI**: Dark-themed 'ExoExplore' interface with real-time Gauge charts.

## 📂 Project Structure
```
ExoHabit-AI/
├── backend/            # Flask application
│   └── app.py
├── exohabitai/         # Core logic
│   ├── data/           # Data loading & feature engineering
│   └── models/         # Model training script
├── frontend/           # HTML templates
├── static/             # CSS & JS files
├── notebooks/          # Jupyter notebooks & Dataset
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd ExoHabit-AI
   ```

2. **Install dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\Activate
   pip install -r requirements.txt
   ```

3. **Train the model** (Optional, model is already saved)
   ```bash
   python exohabitai/models/train_model.py
   ```

4. **Run the application**
   ```bash
   python backend/app.py
   ```

5. **Access the App**
   Open http://localhost:5000 in your browser.

## 📊 Dataset
The dataset is sourced from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/).

## 🤖 Models Used
- **Random Forest Classifier**
- **XGBoost Classifier** (Evaluation)

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.

