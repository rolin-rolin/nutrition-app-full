#!/usr/bin/env python3
"""
Test script for the recommendation pipeline.
Tests the full flow from user input to snack recommendations.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.recommendation import get_recommendations
from app.db.session import get_db
from app.schemas.recommendation import RecommendationRequest

def test_recommendation_pipeline():
    """Test the full recommendation pipeline."""
    
    # Set a dummy OpenAI API key for testing (need real one for full functionality)
    os.environ["OPENAI_API_KEY"] = "sk-test-key-for-testing"
    
    # Create test requests
    test_cases = [
        {
            "name": "Post-workout recovery for soccer player",
            "request": RecommendationRequest(
                user_query="I just played 90 minutes of soccer and want to recover.",
                age=19,
                weight_kg=70.0,
                sex="male",
                exercise_type="soccer",
                exercise_duration_minutes=90,
                exercise_intensity="high",
                timing="post-workout",
                preferences={
                    "flavor_preferences": ["savory"],
                    "texture_preferences": ["crunchy"],
                    "flavor_exclusions": ["sweet"],
                    "dietary_restrictions": ["vegan"],
                    "ingredient_exclusions": ["peanuts"]
                }
            )
        },
        {
            "name": "Pre-workout fuel for runner",
            "request": RecommendationRequest(
                user_query="I need energy before my morning run.",
                age=28,
                weight_kg=65.0,
                sex="female",
                exercise_type="running",
                exercise_duration_minutes=45,
                exercise_intensity="medium",
                timing="pre-workout",
                preferences={
                    "flavor_preferences": ["sweet"],
                    "texture_preferences": ["smooth"],
                    "dietary_restrictions": ["gluten-free"]
                }
            )
        }
    ]
    
    # Get database session
    db = next(get_db())
    
    try:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*60}")
            print(f"Test Case {i}: {test_case['name']}")
            print(f"{'='*60}")
            
            try:
                # Run the recommendation pipeline
                result = asyncio.run(get_recommendations(test_case['request'], db))
                
                # Display results
                print(f"\nRecommendation Pipeline Completed Successfully!")
                print(f"\nMacro Targets:")
                print(f"   Protein: {result.macro_targets.target_protein}g")
                print(f"   Carbs: {result.macro_targets.target_carbs}g")
                print(f"   Fat: {result.macro_targets.target_fat}g")
                print(f"   Calories: {result.macro_targets.target_calories}")
                print(f"   Electrolytes: {result.macro_targets.target_electrolytes}g")
                
                print(f"\nRecommended Snacks ({len(result.recommended_products)} items):")
                total_protein = 0
                total_carbs = 0
                total_fat = 0
                total_calories = 0
                
                for j, product in enumerate(result.recommended_products, 1):
                    print(f"   {j}. {product.name} ({product.brand})")
                    print(f"      Protein: {product.protein}g, Carbs: {product.carbs}g, Fat: {product.fat}g, Calories: {product.calories}")
                    total_protein += product.protein or 0
                    total_carbs += product.carbs or 0
                    total_fat += product.fat or 0
                    total_calories += product.calories or 0
                
                print(f"\nCombination Totals:")
                print(f"   Protein: {total_protein:.1f}g (Target: {result.macro_targets.target_protein}g)")
                print(f"   Carbs: {total_carbs:.1f}g (Target: {result.macro_targets.target_carbs}g)")
                print(f"   Fat: {total_fat:.1f}g (Target: {result.macro_targets.target_fat}g)")
                print(f"   Calories: {total_calories:.0f} (Target: {result.macro_targets.target_calories})")
                
                print(f"\nReasoning:")
                print(result.reasoning)
                
            except Exception as e:
                print(f"Error in test case {i}: {e}")
                import traceback
                traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing Recommendation Pipeline")
    print("Make sure you:")
    print("1. Run 'python init_db.py' to initialize the database")
    print("2. Set OPENAI_API_KEY in the environment or .env file")
    print("3. Have the required dependencies installed")
    print("\nStarting tests...")
    
    test_recommendation_pipeline()
    print("\nTesting complete!") 