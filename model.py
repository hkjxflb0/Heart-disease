# models.py
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import Optional

class PredictionData(BaseModel):
    age: int
    sex: str
    chest_pain_type: str
    resting_blood_pressure: int
    cholestoral: int
    fasting_blood_sugar: str
    rest_ecg: str
    max_heart_rate: int
    exercise_induced_angina: str
    oldpeak: float
    slope: str
    vessels_colored_by_fluoroscopy: str
    thalassemia: str
    prediction: str


class HeartDiseasePrediction(BaseModel):
    prediction: str
    confidence: Optional[float] = None