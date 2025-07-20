#!/usr/bin/env python3
"""
Test the recommendation pipeline logic branching:
1. Full activity info (macro optimization)
2. Only flavor/texture (vector search)
3. Only calorie cap (filtering)
4. Only user_query (fallback)
"""
import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.schemas.recommendation import RecommendationRequest
from app.core.recommendation import get_recommendations

async def test_branching_pipeline():
    print("=== Branching Recommendation Pipeline Test ===\n")
    db = SessionLocal()
    try:
        scenarios = [
            {
                "name": "Full Activity Info (Macro Optimization)",
                "request": RecommendationRequest(
                    user_query="I want a high protein snack after my 60 min strength workout",
                    age=28,
                    exercise_type="strength",
                    exercise_duration_minutes=60,
                    preferences={"flavor_preferences": ["sweet"]}
                )
            },
            {
                "name": "Flavor/Texture Only (Vector Search)",
                "request": RecommendationRequest(
                    user_query="I want something crunchy and savory",
                    preferences={"texture_preferences": ["crunchy"], "flavor_preferences": ["savory"]}
                )
            },
            {
                "name": "Calorie Cap Only (Filtering)",
                "request": RecommendationRequest(
                    user_query="I want snacks under 200 calories",
                    preferences={"calorie_cap": 200}
                )
            },
            {
                "name": "User Query Only (Fallback)",
                "request": RecommendationRequest(
                    user_query="Recommend me a snack"
                )
            }
        ]
        for scenario in scenarios:
            print(f"\n--- {scenario['name']} ---")
            response = await get_recommendations(scenario["request"], db)
            print("Reasoning:")
            print(response.reasoning)
            print("Products:")
            for i, product in enumerate(response.recommended_products):
                pd = product.model_dump()
                print(f"  {i+1}. {pd.get('name', '[no name]')} | Calories: {pd.get('calories', '[n/a]')} | Protein: {pd.get('protein', '[n/a]')}g | Carbs: {pd.get('carbs', '[n/a]')}g | Fat: {pd.get('fat', '[n/a]')}g")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_branching_pipeline()) 