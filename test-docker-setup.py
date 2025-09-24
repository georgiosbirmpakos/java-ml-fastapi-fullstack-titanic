#!/usr/bin/env python3
"""
Docker Setup Test Script
This script tests if the Docker setup is working correctly.
"""

import requests
import time
import sys
from urllib.parse import urljoin

def test_endpoint(url, description, expected_status=200):
    """Test an endpoint and return success status"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            print(f"✅ {description}: {url}")
            return True
        else:
            print(f"❌ {description}: {url} (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {description}: {url} (Error: {e})")
        return False

def test_prediction_api():
    """Test the prediction API with sample data"""
    url = "http://localhost:8000/predict"
    sample_data = {
        "pclass": 1,
        "name": "Mr. John Doe",
        "sex": "male",
        "age": 35.0,
        "sibsp": 0,
        "parch": 0,
        "fare": 50.0,
        "embarked": "S"
    }
    
    try:
        response = requests.post(url, json=sample_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction API: {url}")
            print(f"   Prediction: Survived={result.get('survived')}, Probability={result.get('survival_probability', 0):.3f}")
            return True
        else:
            print(f"❌ Prediction API: {url} (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction API: {url} (Error: {e})")
        return False

def main():
    """Main test function"""
    print("🐳 Testing Docker Setup for Titanic Survival Prediction System")
    print("=" * 60)
    
    # Wait a bit for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(5)
    
    # Test endpoints
    endpoints = [
        ("http://localhost:8000/health", "FastAPI Health Check"),
        ("http://localhost:8000/docs", "FastAPI Documentation"),
        ("http://localhost:8080/", "Java Frontend"),
    ]
    
    results = []
    for url, description in endpoints:
        results.append(test_endpoint(url, description))
    
    # Test prediction API
    results.append(test_prediction_api())
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        print("\n📱 Access the application:")
        print("   Frontend: http://localhost:8080")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        return 0
    else:
        print(f"❌ Some tests failed ({passed}/{total})")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if Docker containers are running: docker-compose ps")
        print("   2. Check container logs: docker-compose logs")
        print("   3. Restart services: docker-compose restart")
        return 1

if __name__ == "__main__":
    sys.exit(main())
