# models.py
from pydantic import BaseModel
from typing import Optional

class HeartDiseaseInput(BaseModel):
    age: int
    sex: int
    chest_pain_type: int
    resting_blood_pressure: int
    cholestoral: int
    fasting_blood_sugar: int
    rest_ecg: int
    max_heart_rate: int
    exercise_induced_angina: int
    oldpeak: float
    slope: int
    vessels_colored_by_flourosopy: int
    thalassemia: int

class HeartDiseasePrediction(BaseModel):
    prediction: str
    confidence: Optional[float] = None