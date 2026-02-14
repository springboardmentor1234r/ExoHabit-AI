# Exoplanet Habitability Prediction API

RESTful API for predicting exoplanet habitability using a trained Random Forest machine learning model.

## Overview

This Flask-based API exposes a trained ML model that predicts whether an exoplanet is habitable based on 10 planetary and stellar features.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Health Check

Check if the API and model are properly loaded.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true
}
```

### 2. List Features

Get a list of required features for prediction.

**Endpoint:** `GET /features`

**Response:**
```json
{
  "required_features": [
    "pl_orbper",
    "pl_rade",
    "pl_bmasse",
    "pl_eqt",
    "st_teff",
    "st_rad",
    "st_mass",
    "sy_dist",
    "sy_snum",
    "sy_pnum"
  ],
  "feature_descriptions": {
    "pl_orbper": "Orbital period (days)",
    "pl_rade": "Planet radius (Earth radii)",
    "pl_bmasse": "Planet mass (Earth masses)",
    "pl_eqt": "Equilibrium temperature (K)",
    "st_teff": "Stellar effective temperature (K)",
    "st_rad": "Stellar radius (Solar radii)",
    "st_mass": "Stellar mass (Solar masses)",
    "sy_dist": "Distance to system (parsec)",
    "sy_snum": "Number of stars in system",
    "sy_pnum": "Number of planets in system"
  },
  "count": 10
}
```

### 3. Single Prediction

Predict habitability for a single exoplanet.

**Endpoint:** `POST /predict`

**Content-Type:** `application/json`

**Request Body:**
```json
{
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
}
```

**Success Response (200):**
```json
{
  "success": true,
  "prediction": {
    "is_habitable": 1,
    "habitability_probability": 0.9876,
    "confidence": "High",
    "classification": "Habitable"
  },
  "input_data": {
    "pl_orbper": 365.25,
    "pl_rade": 1.0,
    ...
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Missing required features: pl_bmasse, pl_eqt"
}
```

### 4. Batch Prediction

Predict habitability for multiple exoplanets in one request.

**Endpoint:** `POST /batch-predict`

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "planets": [
    {
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
    },
    {
      "pl_orbper": 50.0,
      "pl_rade": 5.0,
      "pl_bmasse": 10.0,
      "pl_eqt": 500,
      "st_teff": 6000,
      "st_rad": 1.5,
      "st_mass": 1.2,
      "sy_dist": 100.0,
      "sy_snum": 1,
      "sy_pnum": 3
    }
  ]
}
```

**Success Response (200):**
```json
{
  "success": true,
  "batch_results": [
    {
      "index": 0,
      "success": true,
      "prediction": {
        "is_habitable": 1,
        "habitability_probability": 0.9876,
        "confidence": "High",
        "classification": "Habitable"
      },
      "input_data": {...}
    }
  ],
  "errors": [],
  "total_processed": 2,
  "successful": 2,
  "failed": 0
}
```

**Constraints:**
- Maximum 100 planets per batch request

## Error Handling

The API handles various error scenarios gracefully:

| Status Code | Scenario |
|-------------|----------|
| 200 | Successful prediction |
| 400 | Invalid input (missing/invalid features) |
| 404 | Endpoint not found |
| 500 | Internal server error |
| 503 | Model not loaded |

## Example Usage

### Using cURL

**Single Prediction:**
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

**Health Check:**
```bash
curl http://localhost:5000/health
```

### Using Python

```python
import requests

# Predict habitability
planet_data = {
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
}

response = requests.post(
    "http://localhost:5000/predict",
    json=planet_data
)

result = response.json()
print(f"Habitable: {result['prediction']['is_habitable']}")
print(f"Probability: {result['prediction']['habitability_probability']}")
```

### Using JavaScript/Fetch

```javascript
const predictHabitability = async (planetData) => {
  const response = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(planetData)
  });
  
  return await response.json();
};

// Example usage
const planet = {
  pl_orbper: 365.25,
  pl_rade: 1.0,
  pl_bmasse: 1.0,
  pl_eqt: 288,
  st_teff: 5778,
  st_rad: 1.0,
  st_mass: 1.0,
  sy_dist: 10.0,
  sy_snum: 1,
  sy_pnum: 1
};

predictHabitability(planet)
  .then(result => console.log(result));
```

## Testing

Run the automated test suite:

```bash
python test_api.py
```

This will test all endpoints including:
- Health check
- Feature listing
- Single prediction
- Input validation
- Batch prediction

## Model Information

- **Algorithm:** Random Forest Classifier
- **Features:** 10 planetary and stellar characteristics
- **Output:** Binary classification (0 = Not Habitable, 1 = Habitable)
- **Probability:** Habitability probability score (0-1)

## Feature Descriptions

| Feature | Description | Unit |
|---------|-------------|------|
| pl_orbper | Orbital Period | Days |
| pl_rade | Planet Radius | Earth radii |
| pl_bmasse | Planet Mass | Earth masses |
| pl_eqt | Equilibrium Temperature | Kelvin |
| st_teff | Stellar Effective Temperature | Kelvin |
| st_rad | Stellar Radius | Solar radii |
| st_mass | Stellar Mass | Solar masses |
| sy_dist | System Distance | Parsec |
| sy_snum | Number of Stars | Count |
| sy_pnum | Number of Planets | Count |

## Deployment

### Using Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t exoplanet-api .
docker run -p 5000:5000 exoplanet-api
```

## API Design Notes

1. **RESTful Design:** All endpoints follow REST conventions with appropriate HTTP methods
2. **JSON Format:** All requests and responses use JSON format
3. **Validation:** Comprehensive input validation with detailed error messages
4. **Error Handling:** Graceful error handling with appropriate HTTP status codes
5. **CORS Enabled:** Cross-Origin Resource Sharing enabled for frontend integration
6. **Batch Processing:** Efficient batch endpoint for multiple predictions
7. **Health Monitoring:** Health check endpoint for monitoring and load balancers

## License

This API is part of the Exoplanet ML Pipeline project.
