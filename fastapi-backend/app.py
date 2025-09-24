"""
Clean FastAPI application for Titanic survival prediction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pickle
import os
import sys
import pandas as pd
import numpy as np

# Add the ml-model directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
ml_model_path = os.path.join(current_dir, '..', 'ml-model')
sys.path.insert(0, ml_model_path)

# Change to ml-model directory to load the model
original_cwd = os.getcwd()
os.chdir(ml_model_path)

# Load the trained model and encoders
try:
    with open('models/titanic_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('models/encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    
    with open('models/feature_columns.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    
    print("✅ Model loaded successfully!")
    model_loaded = True
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    encoders = None
    feature_columns = None
    model_loaded = False

# Change back to original directory
os.chdir(original_cwd)

# Initialize FastAPI app
app = FastAPI(
    title="Titanic Survival Prediction API",
    description="A machine learning API for predicting Titanic passenger survival",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PassengerData(BaseModel):
    pclass: int
    name: str
    sex: str
    age: Optional[float] = None
    sibsp: int = 0
    parch: int = 0
    fare: Optional[float] = None
    embarked: str = "S"

class PredictionResult(BaseModel):
    survived: int
    survival_probability: float
    death_probability: float

class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool

# Helper functions
def preprocess_passenger(passenger_data: dict) -> pd.DataFrame:
    """Preprocess passenger data for prediction"""
    df = pd.DataFrame([passenger_data])
    
    # Handle missing values
    df['Age'].fillna(df['Age'].median() if not df['Age'].isna().all() else 30, inplace=True)
    df['Fare'].fillna(df['Fare'].median() if not df['Fare'].isna().all() else 30, inplace=True)
    df['Embarked'].fillna('S', inplace=True)
    
    # Feature engineering
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    
    # Extract title from name
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col',
                                     'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    df['Title'] = df['Title'].replace('Mlle', 'Miss')
    df['Title'] = df['Title'].replace('Ms', 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')
    df['Title'].fillna('Mr', inplace=True)
    
    # Age groups
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 35, 60, 100], 
                           labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
    df['AgeGroup'].fillna('Adult', inplace=True)
    
    # Fare groups
    try:
        df['FareGroup'] = pd.qcut(df['Fare'], q=4, labels=['Low', 'Medium', 'High', 'VeryHigh'], duplicates='drop')
    except ValueError:
        df['FareGroup'] = pd.cut(df['Fare'], bins=4, labels=['Low', 'Medium', 'High', 'VeryHigh'])
    df['FareGroup'].fillna('Medium', inplace=True)
    
    return df

def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical features"""
    df_encoded = df.copy()
    
    # Encode categorical variables
    df_encoded['Sex'] = encoders['sex'].transform(df_encoded['Sex'])
    df_encoded['Embarked'] = encoders['embarked'].transform(df_encoded['Embarked'])
    df_encoded['Title'] = encoders['title'].transform(df_encoded['Title'])
    df_encoded['AgeGroup'] = encoders['age_group'].transform(df_encoded['AgeGroup'])
    df_encoded['FareGroup'] = encoders['fare_group'].transform(df_encoded['FareGroup'])
    
    return df_encoded

# API endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="healthy",
        message="Titanic Survival Prediction API is running",
        model_loaded=model_loaded
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        message="Service is running" + (" and model is loaded" if model_loaded else " but model is not loaded"),
        model_loaded=model_loaded
    )

@app.post("/predict", response_model=PredictionResult)
async def predict_survival(passenger: PassengerData):
    """
    Predict survival for a single passenger
    
    - **pclass**: Passenger class (1, 2, or 3)
    - **name**: Passenger name
    - **sex**: Passenger sex (male or female)
    - **age**: Passenger age (optional)
    - **sibsp**: Number of siblings/spouses aboard
    - **parch**: Number of parents/children aboard
    - **fare**: Ticket fare (optional)
    - **embarked**: Port of embarkation (C, Q, or S)
    """
    if not model_loaded:
        raise HTTPException(
            status_code=503,
            detail="ML model not available"
        )
    
    try:
        # Convert Pydantic model to dictionary
        passenger_dict = {
            'Pclass': passenger.pclass,
            'Name': passenger.name,
            'Sex': passenger.sex,
            'Age': passenger.age,
            'SibSp': passenger.sibsp,
            'Parch': passenger.parch,
            'Fare': passenger.fare,
            'Embarked': passenger.embarked
        }
        
        # Preprocess passenger data
        df_processed = preprocess_passenger(passenger_dict)
        
        # Encode features
        df_encoded = encode_features(df_processed)
        
        # Select features
        X = df_encoded[feature_columns]
        
        # Make prediction
        survival_prob = model.predict_proba(X)[0]
        prediction = model.predict(X)[0]
        
        return PredictionResult(
            survived=int(prediction),
            survival_probability=float(survival_prob[1]),
            death_probability=float(survival_prob[0])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
