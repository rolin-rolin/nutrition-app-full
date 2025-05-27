from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Nutrition Bot API",
    description="API for nutrition recommendations and analysis",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Nutrition Bot API!"} 