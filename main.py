# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import router as heart_router
from config import prediction_collection

app = FastAPI()

# Setting up template rendering
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(heart_router)

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    # Render the HTML form
    return templates.TemplateResponse("form.html", {"request": request})
