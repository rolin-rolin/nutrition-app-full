from pydantic import BaseModel
from typing import List

class UserInput(BaseModel):
    description: str

class RecommendationResponse(BaseModel):
    snacks: List[str]
    reasoning: str 