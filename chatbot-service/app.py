from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.schemas import PredictNLRequest, PredictNLResponse, Passenger
from utils.client import predict_with_backend
from chains.prediction_chain import extract_passenger_from_message

load_dotenv()

app = FastAPI(title="Chatbot Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Request: {request.method} {request.url}")
    print(f"Headers: {dict(request.headers)}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response

class Health(BaseModel):
    status: str

@app.get("/health", response_model=Health)
async def health():
    return Health(status="ok")

@app.get("/test")
async def test_endpoint():
    print("Test endpoint called")
    return {"status": "ok", "message": "Chatbot service is running"}

@app.post("/predict-nl", response_model=PredictNLResponse)
async def predict_nl(req: PredictNLRequest):
    print(f"Received request: {req}")
    print(f"Message: {req.message}")
    print(f"Request type: {type(req)}")
    try:
        extraction = await extract_passenger_from_message(req.message)
        passenger = Passenger(**extraction.passenger.model_dump())
        backend_result = await predict_with_backend(passenger)
        # Generate discussion text
        survived_text = "survived" if int(backend_result["survived"]) else "did not survive"
        survival_pct = float(backend_result["survival_probability"]) * 100
        death_pct = float(backend_result["death_probability"]) * 100
        
        discussion = f"""Based on your description, I've analyzed the passenger information:

**Passenger Details:**
- Name: {passenger.name}
- Class: {passenger.pclass} ({"First" if passenger.pclass == 1 else "Second" if passenger.pclass == 2 else "Third"} class)
- Gender: {passenger.sex.title()}
- Age: {passenger.age if passenger.age else "Unknown"}
- Fare: £{passenger.fare if passenger.fare else "Unknown"}
- Embarked: {passenger.embarked} ({"Cherbourg" if passenger.embarked == "C" else "Queenstown" if passenger.embarked == "Q" else "Southampton"})

**Prediction:**
This passenger {survived_text} the Titanic disaster.

**Confidence:**
- Survival probability: {survival_pct:.1f}%
- Death probability: {death_pct:.1f}%

**Analysis:**
{extraction.reasoning}

The prediction is based on historical data patterns from the Titanic disaster, considering factors like passenger class, age, gender, and fare paid."""
        
        return PredictNLResponse(
            passenger=passenger,
            survived=int(backend_result["survived"]),
            survival_probability=float(backend_result["survival_probability"]),
            death_probability=float(backend_result["death_probability"]),
            reasoning=extraction.reasoning,
            discussion=discussion,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
