from pydantic import BaseModel
from typing import List

"""
Contains pydantic models (data validation/serialization)
"""

class UserInput(BaseModel):
    description: str

class RecommendationResponse(BaseModel):
    snacks: List[str]
    reasoning: str 