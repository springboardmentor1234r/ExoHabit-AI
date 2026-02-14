"""
Test client for the Exoplanet Habitability Prediction API
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_features():
    """Test features endpoint"""
    print("\n" + "="*60)
    print("Testing Features Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/features")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_single_prediction():
    """Test single prediction endpoint with habitable-like planet"""
    print("\n" + "="*60)
    print("Testing Single Prediction (Habitable-like)")
    print("="*60)
    
    # Example data for Earth-like exoplanet
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
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=planet_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_invalid_input():
    """Test prediction with invalid input"""
    print("\n" + "="*60)
    print("Testing Invalid Input Handling")
    print("="*60)
    
    # Missing required fields
    invalid_data = {
        "pl_orbper": 365.25,
        "pl_rade": 1.0
        # Missing other required fields
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 400
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Batch Prediction")
    print("="*60)
    
    planets = [
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
        },
        {
            "pl_orbper": 200.0,
            "pl_rade": 1.5,
            "pl_bmasse": 2.5,
            "pl_eqt": 250,
            "st_teff": 5500,
            "st_rad": 0.9,
            "st_mass": 0.95,
            "sy_dist": 50.0,
            "sy_snum": 1,
            "sy_pnum": 2
        }
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/batch-predict",
            json={"planets": planets},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Total processed: {result.get('total_processed')}")
        print(f"Successful: {result.get('successful')}")
        print(f"Failed: {result.get('failed')}")
        
        for pred in result.get('batch_results', []):
            print(f"\nPlanet {pred['index']}:")
            print(f"  Prediction: {pred['prediction']['classification']}")
            print(f"  Probability: {pred['prediction']['habitability_probability']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("EXOPLANET HABITABILITY API TEST SUITE")
    print("="*60)
    
    tests = [
        ("Health Check", test_health),
        ("Features List", test_features),
        ("Single Prediction", test_single_prediction),
        ("Invalid Input", test_invalid_input),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed_count}/{len(results)} tests passed")


if __name__ == "__main__":
    print("Make sure the Flask server is running on http://localhost:5000")
    print("Start the server with: python app.py")
    
    input("\nPress Enter to start tests...")
    run_all_tests()
