from pydantic import BaseModel, Field
from typing import Optional


class Passenger(BaseModel):
    pclass: int = Field(..., ge=1, le=3)
    name: str
    sex: str
    age: Optional[float] = None
    sibsp: int = 0
    parch: int = 0
    fare: Optional[float] = None
    embarked: str = 'S'


class PredictNLRequest(BaseModel):
    message: str


class PredictNLResponse(BaseModel):
    passenger: Passenger
    survived: int
    survival_probability: float
    death_probability: float
    reasoning: str
    discussion: str = ""  # Make it optional with default empty string
