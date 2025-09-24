"""
Pydantic models for Titanic prediction API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class PassengerClass(str, Enum):
    """Passenger class enumeration"""
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"

class Sex(str, Enum):
    """Sex enumeration"""
    MALE = "male"
    FEMALE = "female"

class Embarked(str, Enum):
    """Embarked port enumeration"""
    CHERBOURG = "C"
    QUEENSTOWN = "Q"
    SOUTHAMPTON = "S"

class PassengerData(BaseModel):
    """Single passenger data model"""
    pclass: PassengerClass = Field(..., description="Passenger class (1, 2, or 3)")
    name: str = Field(..., description="Passenger name")
    sex: Sex = Field(..., description="Passenger sex")
    age: Optional[float] = Field(None, description="Passenger age")
    sibsp: int = Field(0, ge=0, le=8, description="Number of siblings/spouses aboard")
    parch: int = Field(0, ge=0, le=6, description="Number of parents/children aboard")
    fare: Optional[float] = Field(None, ge=0, description="Ticket fare")
    embarked: Embarked = Field(Embarked.SOUTHAMPTON, description="Port of embarkation")

    class Config:
        json_schema_extra = {
            "example": {
                "pclass": "1",
                "name": "Mr. John Doe",
                "sex": "male",
                "age": 35.0,
                "sibsp": 0,
                "parch": 0,
                "fare": 50.0,
                "embarked": "S"
            }
        }

class PredictionResult(BaseModel):
    """Prediction result model"""
    survived: int = Field(..., description="Predicted survival (0 = died, 1 = survived)")
    survival_probability: float = Field(..., ge=0, le=1, description="Probability of survival")
    death_probability: float = Field(..., ge=0, le=1, description="Probability of death")

    class Config:
        json_schema_extra = {
            "example": {
                "survived": 1,
                "survival_probability": 0.75,
                "death_probability": 0.25
            }
        }

class BatchPredictionRequest(BaseModel):
    """Batch prediction request model"""
    passengers: List[PassengerData] = Field(..., description="List of passengers to predict")

    class Config:
        json_schema_extra = {
            "example": {
                "passengers": [
                    {
                        "pclass": "1",
                        "name": "Mr. John Doe",
                        "sex": "male",
                        "age": 35.0,
                        "sibsp": 0,
                        "parch": 0,
                        "fare": 50.0,
                        "embarked": "S"
                    },
                    {
                        "pclass": "3",
                        "name": "Miss Jane Smith",
                        "sex": "female",
                        "age": 25.0,
                        "sibsp": 1,
                        "parch": 0,
                        "fare": 15.0,
                        "embarked": "Q"
                    }
                ]
            }
        }

class BatchPredictionResult(BaseModel):
    """Batch prediction result model"""
    predictions: List[PredictionResult] = Field(..., description="List of prediction results")
    total_passengers: int = Field(..., description="Total number of passengers predicted")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Service message")
    version: str = Field(..., description="API version")
