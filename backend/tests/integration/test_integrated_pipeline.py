#!/usr/bin/env python3
"""
Test the complete integrated recommendation pipeline.

This script tests the full recommendation engine with Layer 1 + Layer 2 integration.
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.schemas.recommendation import RecommendationRequest
from app.core.recommendation import get_recommendations

async def test_integrated_pipeline():
    """Test the complete integrated recommendation pipeline."""
    
    print("=== Integrated Recommendation Pipeline Testing ===\n")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Test scenarios
        test_scenarios = [
            {
                "name": "High Protein Sweet Snack",
                "request": RecommendationRequest(
                    user_query="I want a sweet high protein snack like a protein bar or yogurt",
                    age=25,
                    exercise_type="strength",
                    exercise_duration_minutes=60,
                    preferences={
                        "flavor_preferences": ["sweet"],
                        "dietary_restrictions": ["high-protein"]
                    }
                )
            },
            {
                "name": "Vegan Post-Workout",
                "request": RecommendationRequest(
                    user_query="I need a vegan snack for after my workout, maybe trail mix or hummus",
                    age=30,
                    exercise_type="cardio",
                    exercise_duration_minutes=45,
                    preferences={
                        "dietary_restrictions": ["vegan"],
                        "timing": "post-workout"
                    }
                )
            },
            {
                "name": "Calorie Cap Test",
                "request": RecommendationRequest(
                    user_query="I want snacks under 300 calories total",
                    age=22,
                    exercise_type="cardio",
                    exercise_duration_minutes=30,
                    preferences={
                        "calorie_cap": 300
                    }
                )
            }
        ]
        for scenario in test_scenarios:
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
    asyncio.run(test_integrated_pipeline()) 