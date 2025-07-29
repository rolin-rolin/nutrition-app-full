from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse, EnhancedRecommendationResponse
from app.core.recommendation import get_recommendations
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=EnhancedRecommendationResponse)
async def recommend(request: RecommendationRequest, db: Session = Depends(get_db)):
    """
    Get snack recommendations based on user context and preferences.

    This endpoint handles the entire recommendation process:
    1. Generates macro targets based on user's exercise and physical data.
    2. Augments a search query with soft preferences (flavor, texture).
    3. Simulates vector search for relevant products.
    4. Applies hard filters for strict constraints (dietary, ingredients).
    
    """
    recommendations = await get_recommendations(request, db)
    return recommendations 