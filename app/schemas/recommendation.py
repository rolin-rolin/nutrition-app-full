from pydantic import BaseModel
from typing import List, Optional, Dict, Any

"""
Contains pydantic models (data validation/serialization)
"""

class UserInput(BaseModel):
    description: str
    preferences: Optional[Dict[str, Any]] = None

class RecommendationResponse(BaseModel):
    snacks: List[str]
    reasoning: str 