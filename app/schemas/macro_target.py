from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

"""
Pydantic models for macro targeting functionality
"""

class MacroTargetRequest(BaseModel):
    """Request model for macro targeting"""
    user_query: str
    age: Optional[int] = None
    weight_kg: Optional[float] = None
    sex: Optional[str] = None  # 'male', 'female', 'other'
    exercise_type: Optional[str] = None
    exercise_duration_minutes: Optional[int] = None
    exercise_intensity: Optional[str] = None  # 'low', 'medium', 'high'
    timing: Optional[str] = None  # 'pre-workout', 'post-workout', 'general'

class MacroTargetResponse(BaseModel):
    """Response model for macro targeting"""
    target_calories: Optional[float] = None
    target_protein: Optional[float] = None
    target_carbs: Optional[float] = None
    target_fat: Optional[float] = None
    target_electrolytes: Optional[float] = None
    
    # Timing breakdown
    pre_workout_macros: Optional[Dict[str, Any]] = None
    during_workout_macros: Optional[Dict[str, Any]] = None
    post_workout_macros: Optional[Dict[str, Any]] = None
    
    reasoning: str
    rag_context: str
    confidence_score: Optional[float] = None
    created_at: datetime

class MacroTargetWithUserInput(BaseModel):
    """Complete response including user input and macro targets"""
    user_input: MacroTargetRequest
    macro_targets: MacroTargetResponse 