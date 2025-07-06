from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os

from app.schemas.macro_target import MacroTargetRequest, MacroTargetResponse
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput, MacroTarget
from app.db.session import get_db

router = APIRouter()

def get_macro_targeting_service():
    """Dependency to get macro targeting service"""
    return MacroTargetingServiceLocal()

@router.post("/", response_model=MacroTargetResponse)
async def get_macro_targets(
    request: MacroTargetRequest,
    db: Session = Depends(get_db),
    service: MacroTargetingServiceLocal = Depends(get_macro_targeting_service)
):
    """
    Get macro targets based on user input using RAG pipeline.
    
    This endpoint uses the RAG system to generate personalized macro recommendations
    based on the user's context (age, weight, exercise type, etc.) and stores
    the results in the database.
    """
    try:
        # Create user input record
        user_input = UserInput(
            user_query=request.user_query,
            age=request.age,
            weight_kg=request.weight_kg,
            sex=request.sex,
            exercise_type=request.exercise_type,
            exercise_duration_minutes=request.exercise_duration_minutes,
            exercise_intensity=request.exercise_intensity,
            timing=request.timing
        )
        db.add(user_input)
        db.commit()
        db.refresh(user_input)
        
        # Generate macro targets
        macro_target = service.create_or_update_macro_targets(user_input, db)
        
        # Convert to response model
        response = MacroTargetResponse(
            target_calories=macro_target.target_calories,
            target_protein=macro_target.target_protein,
            target_carbs=macro_target.target_carbs,
            target_fat=macro_target.target_fat,
            target_electrolytes=macro_target.target_electrolytes,
            reasoning=macro_target.reasoning,
            rag_context=macro_target.rag_context,
            confidence_score=macro_target.confidence_score,
            created_at=macro_target.created_at
        )
        
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating macro targets: {str(e)}")

@router.get("/history/{user_input_id}", response_model=MacroTargetResponse)
async def get_macro_target_history(
    user_input_id: int,
    db: Session = Depends(get_db)
):
    """
    Get macro targets for a specific user input from history.
    """
    macro_target = db.query(MacroTarget).filter(MacroTarget.user_input_id == user_input_id).first()
    
    if not macro_target:
        raise HTTPException(status_code=404, detail="Macro targets not found")
    
    return MacroTargetResponse(
        target_calories=macro_target.target_calories,
        target_protein=macro_target.target_protein,
        target_carbs=macro_target.target_carbs,
        target_fat=macro_target.target_fat,
        target_electrolytes=macro_target.target_electrolytes,
        reasoning=macro_target.reasoning,
        rag_context=macro_target.rag_context,
        confidence_score=macro_target.confidence_score,
        created_at=macro_target.created_at
    ) 