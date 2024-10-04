# routes.py
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import joblib

from config import prediction_collection
from model import PredictionData

router = APIRouter()

# Load the trained model
model = joblib.load("C:/Users/rohit.mishra/Documents/GitHub/Heart-disease/final_model.pkl")

# Set up template directory
templates = Jinja2Templates(directory="templates")
sex_map = {
    "Male": 1,
    "Female": 0
}
chest_pain_map = {
    "Typical angina": 1,
    "Atypical angina": 2,
    "Non-anginal pain": 3,
    "Asymptomatic": 4
}
blood_sugar_map = {
    "Lower than 120 mg/ml": 0,
    "Greater than 120 mg/ml": 1
}
rest_ecg_map = {
    "Normal": 0,
    "ST-T wave abnormality": 1,
    "Left ventricular hypertrophy": 2,
}
exercise_angina_map = {
    "Yes": 1,
    "No": 0
}
slope_map = {
    "Upsloping": 1,
    "Flat": 2,
    "Downsloping": 3
}
fluoroscopy_map = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4
}
thalassemia_map = {
    "No": 0,
    "Normal": 3,
    "Fixed Defect": 6,
    "Reversable Defect": 7
}


@router.post("/predict")
async def predict_heart_disease(request: Request,
                                age: int = Form(...),
                                sex: str = Form(...),
                                chest_pain_type: str = Form(...),
                                resting_blood_pressure: int = Form(...),
                                cholestoral: int = Form(...),
                                fasting_blood_sugar: str = Form(...),
                                rest_ecg: str = Form(...),
                                max_heart_rate: int = Form(...),
                                exercise_induced_angina: str = Form(...),
                                oldpeak: float = Form(...),
                                slope: str = Form(...),
                                vessels_colored_by_fluoroscopy: str = Form(...),
                                thalassemia: str = Form(...)):
    sex_num = sex_map[sex]
    chest_pain_num = chest_pain_map[chest_pain_type]
    blood_sugar_num = blood_sugar_map[fasting_blood_sugar]
    rest_ecg_num = rest_ecg_map[rest_ecg]
    exercise_angina_num = exercise_angina_map[exercise_induced_angina]
    slope_num = slope_map[slope]
    fluoroscopy_num = fluoroscopy_map[vessels_colored_by_fluoroscopy]
    thalassemia_num = thalassemia_map[thalassemia]

    # Prepare input for the model
    input_features = [[age, sex_num, chest_pain_num, resting_blood_pressure, cholestoral,
                 blood_sugar_num, rest_ecg_num, max_heart_rate, exercise_angina_num,
                 oldpeak, slope_num, fluoroscopy_num, thalassemia_num]]


    # Make prediction
    prediction = model.predict(input_features)[0]
    confidence = max(model.predict_proba(input_features)[0]) if hasattr(model, 'predict_proba') else None

    result = "Disease" if prediction == 1 else "No Disease"
    print(result)

    prediction_data = PredictionData(
        age=age,
        sex=sex,
        chest_pain_type=chest_pain_type,
        resting_blood_pressure=resting_blood_pressure,
        cholestoral=cholestoral,
        fasting_blood_sugar=fasting_blood_sugar,
        rest_ecg=rest_ecg,
        max_heart_rate=max_heart_rate,
        exercise_induced_angina=exercise_induced_angina,
        oldpeak=oldpeak,
        slope=slope,
        vessels_colored_by_fluoroscopy=vessels_colored_by_fluoroscopy,
        thalassemia=thalassemia,
        prediction="Heart Disease" if prediction == 1 else "No Heart Disease"
    )
    await prediction_collection.insert_one(prediction_data.dict())
    return templates.TemplateResponse("form.html", {
        "request": request,
        "result": result,
        "confidence": confidence
    })
