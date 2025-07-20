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
            print(f"\n--- Scenario: {scenario['name']} ---")
            print(f"User Input: '{scenario['request'].user_query}'")
            print(f"Preferences: {scenario['request'].preferences}")
            
            # Get recommendations
            response = await get_recommendations(scenario['request'], db)
            
            print(f"\n  Results:")
            print(f"    Selected {len(response.recommended_products)} snacks:")
            for i, product in enumerate(response.recommended_products):
                pd = product.model_dump()
                if i == 0:
                    print(f"      [DEBUG] Product model_dump: {pd}")
                print(f"      {i+1}. {pd.get('name', '[no name]')}")
                print(f"         Protein: {pd.get('protein')}g, Carbs: {pd.get('carbs')}g, "
                      f"Fat: {pd.get('fat')}g, Electrolytes: {pd.get('electrolytes_mg', '[n/a]')}mg")
            
            # Show macro targets
            if response.macro_targets:
                print(f"\n    Macro Targets:")
                print(f"      Protein: {response.macro_targets.target_protein}g")
                print(f"      Carbs: {response.macro_targets.target_carbs}g")
                print(f"      Fat: {response.macro_targets.target_fat}g")
                print(f"      Electrolytes: {response.macro_targets.target_electrolytes}mg")
            
            # Show reasoning
            print(f"\n    Reasoning:")
            for step in response.reasoning.split('\n'):
                if step.strip():
                    print(f"      - {step.strip()}")
            
            print(f"\n" + "="*80)
        
        # Test randomization by running the same query multiple times
        print(f"\n--- Randomization Test ---")
        print(f"Running the same query 3 times to test variety...")
        
        test_request = RecommendationRequest(
            user_query="I want a sweet high protein snack like a protein bar or yogurt",
            preferences={
                "flavor_preferences": ["sweet"],
                "dietary_restrictions": ["high-protein"]
            }
        )
        
        results = []
        for run in range(3):
            print(f"\n  Run {run + 1}:")
            response = await get_recommendations(test_request, db)
            
            product_names = [p.model_dump().get('name', '[no name]') for p in response.recommended_products]
            print(f"    Selected: {', '.join(product_names)}")
            
            results.append({
                'run': run + 1,
                'products': product_names,
                'count': len(response.recommended_products)
            })
        
        # Analyze variety
        print(f"\n  Randomization Analysis:")
        unique_combinations = set()
        for result in results:
            combination_key = tuple(sorted(result['products']))
            unique_combinations.add(combination_key)
        
        print(f"    Unique combinations: {len(unique_combinations)} out of {len(results)} runs")
        print(f"    Variety percentage: {(len(unique_combinations) / len(results)) * 100:.1f}%")
        
        if len(unique_combinations) > 1:
            print(f"    All unique combinations:")
            for i, combination in enumerate(sorted(unique_combinations)):
                print(f"      {i+1}. {', '.join(combination)}")
        
        print(f"\n=== Integrated Pipeline Test Complete ===")
        
    except Exception as e:
        print(f"Error testing integrated pipeline: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_integrated_pipeline()) 