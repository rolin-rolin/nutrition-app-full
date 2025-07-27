from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from pydantic import BaseModel

from app.schemas.macro_target import MacroTargetRequest, MacroTargetResponse, MacroTargetWithUserInput
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput, MacroTarget
from app.db.session import get_db

router = APIRouter()

class NaturalLanguageRequest(BaseModel):
    """Request model for natural language macro targeting"""
    user_query: str

def get_macro_targeting_service():
    """Dependency to get macro targeting service"""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return MacroTargetingServiceLocal(
        rag_store_path="../rag_store", 
        openai_api_key=openai_api_key
    )

@router.post("/natural", response_model=MacroTargetWithUserInput)
async def get_macro_targets_from_natural_language(
    request: NaturalLanguageRequest,
    db: Session = Depends(get_db),
    service: MacroTargetingServiceLocal = Depends(get_macro_targeting_service)
):
    """
    Get macro targets from natural language query using LLM field extraction.
    
    This endpoint uses OpenAI's LLM to extract structured fields from a natural language
    query, then generates personalized macro recommendations using the RAG pipeline.
    
    Example query: "I'm an 18-year-old guy, weigh 160 pounds. I want savory, chewy snacks 
    for my 90-minute soccer match to fuel recovery. I'm lactose intolerant and I'd like 
    to be gluten-free. Keep it under 400 calories"
    """
    try:
        # Use the enhanced service to extract fields and generate macro targets
        user_input, macro_target = service.generate_macro_targets_from_query(request.user_query, db)
        
        # Convert to response models
        user_input_response = MacroTargetRequest(
            user_query=user_input.user_query,
            age=user_input.age,
            weight_kg=user_input.weight_kg,
            sex=user_input.sex,
            exercise_type=user_input.exercise_type,
            exercise_duration_minutes=user_input.exercise_duration_minutes,
            exercise_intensity=user_input.exercise_intensity,
            timing=user_input.timing
        )
        
        macro_target_response = MacroTargetResponse(
            target_calories=macro_target.target_calories,
            target_protein=macro_target.target_protein,
            target_carbs=macro_target.target_carbs,
            target_fat=macro_target.target_fat,
            target_electrolytes=macro_target.target_electrolytes,
            pre_workout_macros=macro_target.pre_workout_macros,
            during_workout_macros=macro_target.during_workout_macros,
            post_workout_macros=macro_target.post_workout_macros,
            reasoning=macro_target.reasoning,
            rag_context=macro_target.rag_context,
            confidence_score=macro_target.confidence_score,
            created_at=macro_target.created_at
        )
        
        return MacroTargetWithUserInput(
            user_input=user_input_response,
            macro_targets=macro_target_response
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating macro targets from natural language: {str(e)}")

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
            pre_workout_macros=macro_target.pre_workout_macros,
            during_workout_macros=macro_target.during_workout_macros,
            post_workout_macros=macro_target.post_workout_macros,
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
        pre_workout_macros=macro_target.pre_workout_macros,
        during_workout_macros=macro_target.during_workout_macros,
        post_workout_macros=macro_target.post_workout_macros,
        reasoning=macro_target.reasoning,
        rag_context=macro_target.rag_context,
        confidence_score=macro_target.confidence_score,
        created_at=macro_target.created_at
    ) 