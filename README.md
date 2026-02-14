# ExoHabit AI 🌌

An intelligent system designed to predict the habitability potential of exoplanets using machine learning.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-orange.svg)

## 🚀 Overview

**ExoHabit-AI** analyzes complex planetary and stellar parameters (such as mass, radius, orbital period, and distance from the host star) to determine which distant worlds might support life. The system features an interactive web interface with 3D visualizations and real-time predictions.

### Key Features

- 🤖 **Machine Learning Models** - Trained on NASA Exoplanet Archive data
- 🎨 **Interactive 3D Visualizations** - Three.js powered space animations
- 📊 **Real-time Predictions** - Instant habitability analysis
- 📱 **Responsive Design** - Works on all devices
- 🌐 **RESTful API** - Easy integration with other applications

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web framework for API and frontend
- **Scikit-learn** - Machine learning models (Random Forest, XGBoost)
- **Joblib** - Model serialization
- **Pandas/NumPy** - Data processing

### Frontend
- **HTML5/CSS3** - Modern semantic markup
- **JavaScript (ES6+)** - Interactive features
- **Three.js** - 3D graphics and starfield animations
- **Chart.js** - Data visualization and charts
- **GSAP** - Advanced scroll animations

### Data Visualization
- **Matplotlib** - Static plots and charts
- **Seaborn** - Statistical visualizations

## 📁 Project Structure

```
ExoHabit-AI/
├── backend/
│   ├── app.py                      # Flask API server
│   ├── Random_Forest_model.joblib  # Trained ML model
│   └── scaler.joblib               # Data scaler
├── frontend/
│   ├── static/
│   │   ├── styles.css             # Application styles
│   │   └── app.js                 # Frontend JavaScript
│   └── templates/
│       ├── index.html             # Main website
│       └── test_sections.html     # Testing page
├── models/                         # Additional ML models
│   ├── XGBoost_model.joblib
│   └── Logistic_Regression_model.joblib
├── data/
│   ├── raw/                        # Raw datasets
│   └── processed/                  # Cleaned data
├── notebooks/                      # Jupyter notebooks
│   ├── exoplanet_pipeline.ipynb
│   └── Exoplanet_preprocessing.ipynb
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
└── README.md                       # This file
```

## 📈 Project Status

- [x] **Phase 0:** Project Initialization & Environment Setup
- [x] **Milestone 1:** Data Exploration & Preliminary Analysis (Completed)
- [x] **Milestone 2:** Data Preprocessing & Feature Engineering (Completed)
- [x] **Milestone 3:** ML Model Training & Evaluation
- [x] **Milestone 4:** Web Application Development
- [ ] **Milestone 5:** Deployment & Documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ExoHabit-AI.git
   cd ExoHabit-AI
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   cd backend
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 💻 Usage

### Web Interface

1. Visit `http://localhost:5000` to explore the interactive website
2. Learn about famous exoplanets in the encyclopedia sections
3. Navigate to "Predict Habitability" to use the ML model
4. Enter exoplanet parameters or use quick presets (Earth, Mars, Jupiter, Proxima b)
5. Get instant habitability predictions with confidence scores

### API Usage

The application exposes RESTful API endpoints:

#### Check API Health
```bash
curl http://localhost:5000/health
```

#### Get Required Features
```bash
curl http://localhost:5000/features
```

#### Make a Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pl_orbper": 365.25,
    "pl_rade": 1.0,
    "pl_bmasse": 1.0,
    "pl_eqt": 288,
    "st_teff": 5778,
    "st_rad": 1.0,
    "st_mass": 1.0,
    "sy_dist": 10.0,
    "sy_snum": 1,
    "sy_pnum": 1
  }'
```

#### Response Format
```json
{
  "success": true,
  "prediction": {
    "is_habitable": 1,
    "habitability_probability": 0.85,
    "confidence": "High",
    "classification": "Habitable"
  },
  "input_data": { ... }
}
```

## 📊 Input Features

The ML model requires the following 10 features:

| Feature | Description | Unit | Example |
|---------|-------------|------|---------|
| `pl_orbper` | Orbital Period | days | 365.25 |
| `pl_rade` | Planet Radius | Earth radii | 1.0 |
| `pl_bmasse` | Planet Mass | Earth masses | 1.0 |
| `pl_eqt` | Equilibrium Temperature | K | 288 |
| `st_teff` | Stellar Temperature | K | 5778 |
| `st_rad` | Stellar Radius | Solar radii | 1.0 |
| `st_mass` | Stellar Mass | Solar masses | 1.0 |
| `sy_dist` | System Distance | parsec | 10.0 |
| `sy_snum` | Number of Stars | count | 1 |
| `sy_pnum` | Number of Planets | count | 1 |

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main website |
| `/api` | GET | API documentation |
| `/health` | GET | Server health check |
| `/features` | GET | Required feature list |
| `/predict` | POST | Single prediction |
| `/batch-predict` | POST | Batch predictions (max 100) |

## 🤖 Model Training

The system uses a Random Forest classifier trained on the NASA Exoplanet Archive dataset:

- **Algorithm:** Random Forest with 100 estimators
- **Preprocessing:** StandardScaler for feature normalization
- **Validation:** Cross-validation for robust performance metrics
- **Metrics:** Accuracy, Precision, Recall, F1-Score

See the `notebooks/` directory for detailed training notebooks and analysis.

## 🧪 Testing

Run the test script to verify the API:
```bash
cd backend
python test_api.py
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Add docstrings to functions
- Update tests for new features
- Update documentation as needed

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA Exoplanet Archive** for providing the dataset
- **NASA's Kepler and TESS missions** for discovering thousands of exoplanets
- **The open-source community** for amazing tools and libraries
- **Scikit-learn team** for the excellent ML framework

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Project Link: [https://github.com/yourusername/ExoHabit-AI](https://github.com/yourusername/ExoHabit-AI)

---

Built with ❤️ and ☕ for space enthusiasts everywhere 🚀

*"The universe is not only queerer than we suppose, but queerer than we can suppose."* - J.B.S. Haldane
