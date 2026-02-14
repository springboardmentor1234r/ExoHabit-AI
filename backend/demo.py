"""
Demo script showing API usage examples with sample data
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def demo_api():
    """Demonstrate API usage with examples"""
    
    print("="*70)
    print("EXOPLANET HABITABILITY PREDICTION API - DEMO")
    print("="*70)
    
    # Example 1: Check API health
    print("\n1. Checking API Health...")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"GET {BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure the Flask server is running: python app.py")
        return
    
    # Example 2: Get required features
    print("\n2. Getting Required Features...")
    print("-" * 70)
    response = requests.get(f"{BASE_URL}/features")
    print(f"GET {BASE_URL}/features")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Required Features ({data['count']} total):")
    for feature, desc in data['feature_descriptions'].items():
        print(f"  • {feature}: {desc}")
    
    # Example 3: Predict Earth-like exoplanet
    print("\n3. Predicting Earth-like Exoplanet...")
    print("-" * 70)
    earth_like = {
        "pl_orbper": 365.25,    # 365.25 day orbit
        "pl_rade": 1.0,          # 1 Earth radius
        "pl_bmasse": 1.0,        # 1 Earth mass
        "pl_eqt": 288,           # 288K equilibrium temp
        "st_teff": 5778,         # Sun-like star
        "st_rad": 1.0,           # 1 Solar radius
        "st_mass": 1.0,          # 1 Solar mass
        "sy_dist": 10.0,         # 10 parsecs away
        "sy_snum": 1,            # Single star system
        "sy_pnum": 1             # 1 planet in system
    }
    
    print(f"POST {BASE_URL}/predict")
    print(f"Input Data: {json.dumps(earth_like, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=earth_like,
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    print(f"\nStatus: {response.status_code}")
    print(f"Prediction: {result['prediction']['classification']}")
    print(f"Probability: {result['prediction']['habitability_probability']:.2%}")
    print(f"Confidence: {result['prediction']['confidence']}")
    
    # Example 4: Predict Hot Jupiter
    print("\n4. Predicting Hot Jupiter (Non-habitable)...")
    print("-" * 70)
    hot_jupiter = {
        "pl_orbper": 3.5,        # Very short orbit
        "pl_rade": 11.0,         # 11 Earth radii (Jupiter-sized)
        "pl_bmasse": 318.0,      # Jupiter mass
        "pl_eqt": 1200,          # Very hot
        "st_teff": 6000,         # Hot star
        "st_rad": 1.1,           # Slightly larger than Sun
        "st_mass": 1.05,         # Slightly more massive than Sun
        "sy_dist": 50.0,         # 50 parsecs away
        "sy_snum": 1,            # Single star
        "sy_pnum": 1             # 1 planet
    }
    
    print(f"POST {BASE_URL}/predict")
    print(f"Input Data: {json.dumps(hot_jupiter, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=hot_jupiter,
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    print(f"\nStatus: {response.status_code}")
    print(f"Prediction: {result['prediction']['classification']}")
    print(f"Probability: {result['prediction']['habitability_probability']:.2%}")
    print(f"Confidence: {result['prediction']['confidence']}")
    
    # Example 5: Batch prediction
    print("\n5. Batch Prediction (3 planets)...")
    print("-" * 70)
    
    planets = [
        earth_like,
        hot_jupiter,
        {
            "pl_orbper": 200.0,     # 200 day orbit
            "pl_rade": 1.5,          # 1.5 Earth radii
            "pl_bmasse": 2.5,        # 2.5 Earth masses
            "pl_eqt": 250,           # 250K (colder than Earth)
            "st_teff": 5500,         # Cooler star
            "st_rad": 0.9,           # Smaller star
            "st_mass": 0.95,         # Less massive star
            "sy_dist": 25.0,         # 25 parsecs away
            "sy_snum": 1,            # Single star
            "sy_pnum": 2             # 2 planets
        }
    ]
    
    print(f"POST {BASE_URL}/batch-predict")
    print(f"Batch Size: {len(planets)} planets")
    
    response = requests.post(
        f"{BASE_URL}/batch-predict",
        json={"planets": planets},
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    print(f"\nStatus: {response.status_code}")
    print(f"Total Processed: {result['total_processed']}")
    print(f"Successful: {result['successful']}")
    print(f"Failed: {result['failed']}")
    
    print("\nPredictions:")
    for pred in result['batch_results']:
        p = pred['prediction']
        print(f"  Planet {pred['index']}: {p['classification']} "
              f"(prob: {p['habitability_probability']:.2%}, "
              f"confidence: {p['confidence']})")
    
    # Example 6: Invalid input handling
    print("\n6. Testing Invalid Input Handling...")
    print("-" * 70)
    
    invalid_data = {
        "pl_orbper": 365.25,
        "pl_rade": "invalid"  # String instead of number
    }
    
    print(f"POST {BASE_URL}/predict")
    print(f"Input Data: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=invalid_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Error: {response.json()['error']}")
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nTo test the API manually:")
    print("  1. Start the server: python app.py")
    print("  2. Run tests: python test_api.py")
    print("  3. Read the docs: API.md")


if __name__ == "__main__":
    print("Make sure the Flask server is running on http://localhost:5000")
    print("Start it with: python app.py")
    print()
    
    try:
        input("Press Enter to start the demo...")
        demo_api()
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
