import requests
import json

# Test the backend predict endpoint
url = "http://localhost:8000/predict"
data = {
    "pclass": 1,
    "name": "Test",
    "sex": "male",
    "age": 35,
    "sibsp": 0,
    "parch": 0,
    "fare": 50,
    "embarked": "S"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
