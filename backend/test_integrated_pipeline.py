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
                "name": "Pre-Workout Energy Boost",
                "request": RecommendationRequest(
                    user_input="I need a pre-workout snack that gives me energy and protein for my strength training session",
                    preferences={
                        "dietary_restrictions": [],
                        "flavor_preferences": ["sweet", "chocolate"],
                        "texture_preferences": ["crunchy"],
                        "max_price_usd": 5.0
                    }
                )
            },
            {
                "name": "Post-Workout Recovery",
                "request": RecommendationRequest(
                    user_input="I just finished a long cardio session and need snacks to help with muscle recovery",
                    preferences={
                        "dietary_restrictions": ["vegan"],
                        "flavor_preferences": ["savory"],
                        "texture_preferences": ["smooth", "creamy"]
                    }
                )
            },
            {
                "name": "Low Carb Weight Loss",
                "request": RecommendationRequest(
                    user_input="I'm trying to lose weight and need low carb high protein snacks",
                    preferences={
                        "dietary_restrictions": [],
                        "flavor_preferences": ["savory"],
                        "ingredient_exclusions": ["sugar", "artificial sweeteners"]
                    }
                )
            },
            {
                "name": "Electrolyte Replenishment",
                "request": RecommendationRequest(
                    user_input="I need snacks with electrolytes for hydration after my workout",
                    preferences={
                        "dietary_restrictions": [],
                        "flavor_preferences": ["fruity", "citrus"],
                        "form_preferences": ["liquid", "smoothie"]
                    }
                )
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n--- Scenario: {scenario['name']} ---")
            print(f"User Input: '{scenario['request'].user_input}'")
            print(f"Preferences: {scenario['request'].preferences}")
            
            # Get recommendations
            response = await get_recommendations(scenario['request'], db)
            
            print(f"\n  Results:")
            print(f"    Selected {len(response.recommended_products)} snacks:")
            for i, product in enumerate(response.recommended_products):
                print(f"      {i+1}. {product.name}")
                print(f"         Protein: {product.protein}g, Carbs: {product.carbs}g, "
                      f"Fat: {product.fat}g, Electrolytes: {product.electrolytes_mg}mg")
            
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
            user_input="I need a pre-workout snack with protein and carbs for energy",
            preferences={
                "dietary_restrictions": [],
                "flavor_preferences": ["sweet"]
            }
        )
        
        results = []
        for run in range(3):
            print(f"\n  Run {run + 1}:")
            response = await get_recommendations(test_request, db)
            
            product_names = [p.name for p in response.recommended_products]
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