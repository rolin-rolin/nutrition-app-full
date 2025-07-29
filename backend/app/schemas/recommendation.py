from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from .product import Product
from .macro_target import MacroTargetResponse

"""
Contains pydantic models (data validation/serialization)
"""

class TimingMacroBreakdown(BaseModel):
    """Breakdown of macro targets by timing (pre, during, post workout)."""
    pre_workout: Optional[Dict[str, Any]] = None
    during_workout: Optional[Dict[str, Any]] = None
    post_workout: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)

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

class UserProfileInfo(BaseModel):
    """User profile information for display."""
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    exercise_type: Optional[str] = None
    exercise_duration_minutes: Optional[int] = None
    age_display: str  # e.g., "25 years old" or "using default age 21"
    weight_display: str  # e.g., "70kg" or "using default 70kg weight"
    exercise_display: str  # e.g., "cardio for 60 minutes" or "using default cardio"
    
    model_config = ConfigDict(from_attributes=True)

class BundleStats(BaseModel):
    """Statistics about the recommended bundle."""
    total_protein: float
    total_carbs: float
    total_fat: float
    total_electrolytes: float
    total_calories: float
    num_snacks: int
    target_match_percentage: float
    
    model_config = ConfigDict(from_attributes=True)

class PreferenceInfo(BaseModel):
    """Information about applied preferences and filters."""
    soft_preferences: List[str] = []  # e.g., ["high-protein", "sweet flavor"]
    hard_filters: List[str] = []  # e.g., ["vegan", "no nuts"]
    
    model_config = ConfigDict(from_attributes=True)

class KeyPrinciple(BaseModel):
    """A key principle from the knowledge document."""
    principle: str
    
    model_config = ConfigDict(from_attributes=True)

class EnhancedRecommendationResponse(BaseModel):
    """Enhanced response model with all information needed for frontend display."""
    recommended_products: List[Product]
    macro_targets: Optional[MacroTargetResponse] = None
    timing_breakdown: Optional[TimingMacroBreakdown] = None
    reasoning: str
    
    # New fields for frontend presentation
    user_profile: Optional[UserProfileInfo] = None
    bundle_stats: Optional[BundleStats] = None
    preferences: Optional[PreferenceInfo] = None
    key_principles: List[KeyPrinciple] = []
    
    model_config = ConfigDict(from_attributes=True)

class RecommendationResponse(BaseModel):
    recommended_products: List[Product]
    macro_targets: Optional[MacroTargetResponse] = None
    reasoning: str 

    model_config = ConfigDict(from_attributes=True)