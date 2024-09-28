from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import router as heart_router
from config import db

app = FastAPI()

# Setting up template rendering
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(heart_router)


@app.on_event("startup")
async def startup_db_client():
    print("Connecting to MongoDB...")


@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()
    print("MongoDB connection closed.")


@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# Handling form submission from the frontend
@app.post("/predict", response_class=HTMLResponse)
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
    # Replace this with model prediction logic
    input_features = [[
        age, sex, chest_pain_type, resting_blood_pressure, cholestoral,
        fasting_blood_sugar, rest_ecg, max_heart_rate, exercise_induced_angina,
        oldpeak, slope, vessels_colored_by_flourosopy, thalassemia
    ]]

    # Example: Making a prediction using your model
    model = joblib.load("path_to_your_model.pkl")
    prediction = model.predict(input_features)[0]
    confidence = max(model.predict_proba(input_features)[0]) if hasattr(model, 'predict_proba') else None

    result = "Disease" if prediction == 1 else "No Disease"

    return templates.TemplateResponse("form.html", {
        "request": request,
        "result": result,
        "confidence": confidence
    })