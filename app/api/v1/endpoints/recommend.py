from fastapi import APIRouter
from app.schemas.recommendation import UserInput, RecommendationResponse
from app.core.recommendation import get_recommendations

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def recommend(input: UserInput):
    recommendations = await get_recommendations(input.description)
    return recommendations 