from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from .product import Product
from .macro_target import MacroTargetResponse

"""
Contains pydantic models (data validation/serialization)
"""

class RecommendationRequest(BaseModel):
    """Request model for getting a full snack recommendation."""
    user_query: str
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    sex: Optional[str] = None
    exercise_type: Optional[str] = None
    exercise_duration_minutes: Optional[int] = None
    exercise_intensity: Optional[str] = None
    timing: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None  # calorie_cap is optional, e.g. preferences={"calorie_cap": 300}

    # Logic will branch based on which fields are present (see core/recommendation.py)
    model_config = ConfigDict(from_attributes=True)

class RecommendationResponse(BaseModel):
    recommended_products: List[Product]
    macro_targets: MacroTargetResponse
    reasoning: str 

    model_config = ConfigDict(from_attributes=True)