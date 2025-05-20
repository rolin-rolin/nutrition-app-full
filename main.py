from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    description: str

@app.post("/recommend")
def recommend(input: UserInput):
    # Placeholder for your real logic
    return {
        "snacks": ["protein bar", "trail mix", "hydration drink"],
        "reasoning": f"Based on your input: {input.description}"
    }

@app.get("/")
def root():
    return {"message": "Welcome to the Nutrition App API!"}