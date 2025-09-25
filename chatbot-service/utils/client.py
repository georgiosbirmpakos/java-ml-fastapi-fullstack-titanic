import httpx
from .schemas import Passenger

FASTAPI_BASE_URL = "http://localhost:8000"

async def predict_with_backend(passenger: Passenger) -> dict:
    url = f"{FASTAPI_BASE_URL}/predict"
    payload = {
        "pclass": passenger.pclass,
        "name": passenger.name,
        "sex": passenger.sex,
        "age": passenger.age,
        "sibsp": passenger.sibsp,
        "parch": passenger.parch,
        "fare": passenger.fare,
        "embarked": passenger.embarked,
    }
    print(f"Sending to backend: {payload}")
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload)
        print(f"Backend response status: {resp.status_code}")
        print(f"Backend response body: {resp.text}")
        resp.raise_for_status()
        return resp.json()
