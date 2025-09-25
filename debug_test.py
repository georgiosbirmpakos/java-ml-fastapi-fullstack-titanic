import requests
import json

# Test with minimal data
url = "http://localhost:8000/predict"
data = {
    "pclass": 1,
    "name": "Test",
    "sex": "male",
    "age": 35.0,
    "sibsp": 0,
    "parch": 0,
    "fare": 50.0,
    "embarked": "S"
}

print("Testing backend with data:")
print(json.dumps(data, indent=2))

try:
    response = requests.post(url, json=data)
    print(f"\nStatus Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Success: {response.json()}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
