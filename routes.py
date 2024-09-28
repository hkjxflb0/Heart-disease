# routes.py
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from model import HeartDiseaseInput, HeartDiseasePrediction
# import joblib  # Assuming you're using joblib to load the model

router = APIRouter()

# Load your trained model
# model = joblib.load("path_to_your_model.pkl")

# Set up the template directory
templates = Jinja2Templates(directory="templates")


@router.post("/predict", response_model=HeartDiseasePrediction)
async def predict_heart_disease(request: Request,
                                age: int = Form(...),
                                sex: int = Form(...),
                                chest_pain_type: int = Form(...),
                                resting_blood_pressure: int = Form(...),
                                cholestoral: int = Form(...),
                                fasting_blood_sugar: int = Form(...),
                                rest_ecg: int = Form(...),
                                max_heart_rate: int = Form(...),
                                exercise_induced_angina: int = Form(...),
                                oldpeak: float = Form(...),
                                slope: int = Form(...),
                                vessels_colored_by_flourosopy: int = Form(...),
                                thalassemia: int = Form(...)):
    # Convert form data into input format for model
    input_features = [[
        age, sex, chest_pain_type, resting_blood_pressure, cholestoral,
        fasting_blood_sugar, rest_ecg, max_heart_rate, exercise_induced_angina,
        oldpeak, slope, vessels_colored_by_flourosopy, thalassemia
    ]]

    # Make prediction
    prediction = model.predict(input_features)[0]
    confidence = max(model.predict_proba(input_features)[0]) if hasattr(model, 'predict_proba') else None

    result = "Disease" if prediction == 1 else "No Disease"

    return templates.TemplateResponse("form.html", {
        "request": request,
        "result": result,
        "confidence": confidence
    })
