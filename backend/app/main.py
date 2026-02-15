from fastapi import FastAPI
from backend.app.routes.predict import router as predict_router

app = FastAPI(
    title="AI Pricing Prediction Service",
    description="Industry-grade ML backend for product price prediction",
    version="1.0.0"
)

app.include_router(predict_router)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "pricing-ml-backend"
    }