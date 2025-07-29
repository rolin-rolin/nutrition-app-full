#!/usr/bin/env python3
"""
Example demonstrating the enhanced recommendation response structure.
This shows how the backend provides all the information needed for frontend display.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.schemas.recommendation import RecommendationRequest, EnhancedRecommendationResponse
from app.core.recommendation import get_recommendations
from app.db.session import get_db


async def demonstrate_enhanced_response():
    """Demonstrate the enhanced response structure."""
    
    # Example 1: Full activity info with preferences
    print("=== Example 1: Full Activity Info ===")
    request1 = RecommendationRequest(
        user_query="I need snacks for my cardio workout",
        age=25,
        weight_kg=70.0,
        exercise_type="cardio",
        exercise_duration_minutes=60,
        preferences={
            "flavor_preferences": ["sweet", "fruity"],
            "texture_preferences": ["crunchy"],
            "dietary_requirements": ["vegan"],
            "allergen_restrictions": ["nuts"]
        }
    )
    
    # Get recommendations (this would normally use a real database)
    print("Request:", request1.model_dump())
    print("\nExpected Enhanced Response Structure:")
    
    # Show what the response would contain
    print("""
    {
        "recommended_products": [
            {
                "id": 1,
                "name": "Product Name",
                "protein": 10.0,
                "carbs": 25.0,
                "fat": 5.0,
                "calories": 165.0,
                "electrolytes_mg": 50.0,
                "image_url": "https://...",
                "buy_link": "https://..."
            }
        ],
        "macro_targets": {
            "target_protein": 25.0,
            "target_carbs": 75.0,
            "target_fat": 15.0,
            "target_calories": 500.0,
            "target_electrolytes": 1.0,
            "reasoning": "Calculated for 25-year-old, 70kg individual doing cardio for 60 minutes..."
        },
        "timing_breakdown": {
            "pre_workout": {
                "carbs": 15.0,
                "protein": 5.0,
                "fat": 5.0,
                "calories": 100.0
            },
            "during_workout": {
                "carbs": 10.0,
                "protein": 2.0,
                "fat": 2.0,
                "electrolytes": 50.0,
                "calories": 58.0
            },
            "post_workout": {
                "carbs": 50.0,
                "protein": 18.0,
                "fat": 10.0,
                "calories": 400.0
            }
        },
        "user_profile": {
            "age": 25,
            "weight_kg": 70.0,
            "exercise_type": "cardio",
            "exercise_duration_minutes": 60,
            "age_display": "25 years old",
            "weight_display": "70kg",
            "exercise_display": "cardio for 60 minutes"
        },
        "bundle_stats": {
            "total_protein": 28.5,
            "total_carbs": 78.2,
            "total_fat": 16.8,
            "total_electrolytes": 120.0,
            "total_calories": 485.0,
            "num_snacks": 6,
            "target_match_percentage": 85.2
        },
        "preferences": {
            "soft_preferences": ["sweet flavor", "fruity flavor", "crunchy texture"],
            "hard_filters": ["vegan", "no nuts"]
        },
        "key_principles": [
            {"principle": "Focus on easily digestible carbohydrates before cardio"},
            {"principle": "Include moderate protein for muscle preservation"}
        ],
        "reasoning": "Retrieved RAG context and generated macro targets...\\nLayer 2 optimization selected 6 snacks..."
    }
    """)
    
    # Example 2: Minimal info (defaults used)
    print("\n=== Example 2: Minimal Info (Defaults Used) ===")
    request2 = RecommendationRequest(
        user_query="I need snacks",
        preferences={
            "flavor_preferences": ["sweet"]
        }
    )
    
    print("Request:", request2.model_dump())
    print("\nExpected Response Structure:")
    print("""
    {
        "recommended_products": [...],
        "macro_targets": null,  // No activity info
        "user_profile": null,   // No activity info
        "bundle_stats": null,   // No activity info
        "preferences": {
            "soft_preferences": ["sweet flavor"],
            "hard_filters": []
        },
        "key_principles": [],   // No knowledge document
        "reasoning": "No activity info detected; skipping macro targeting..."
    }
    """)
    
    # Example 3: Strength activity (high-protein detection)
    print("\n=== Example 3: Strength Activity (High-Protein Detection) ===")
    request3 = RecommendationRequest(
        user_query="I need snacks for weightlifting",
        age=30,
        weight_kg=80.0,
        exercise_type="weightlifting",
        exercise_duration_minutes=90,
        preferences={
            "flavor_preferences": ["sweet"]
        }
    )
    
    print("Request:", request3.model_dump())
    print("\nExpected Response Structure:")
    print("""
    {
        "recommended_products": [...],
        "macro_targets": {
            "target_protein": 32.5,  // Higher protein for strength
            "target_carbs": 67.5,    // Slightly lower carbs
            ...
        },
        "timing_breakdown": {
            "pre_workout": {
                "carbs": 20.0,
                "protein": 8.0,
                "fat": 8.0,
                "calories": 180.0
            },
            "during_workout": {
                "carbs": 5.0,
                "protein": 3.0,
                "fat": 1.0,
                "electrolytes": 75.0,
                "calories": 41.0
            },
            "post_workout": {
                "carbs": 42.5,
                "protein": 21.5,
                "fat": 7.0,
                "calories": 320.0
            }
        },
        "user_profile": {
            "age": 30,
            "weight_kg": 80.0,
            "exercise_type": "weightlifting",
            "exercise_duration_minutes": 90,
            "age_display": "30 years old",
            "weight_display": "80kg",
            "exercise_display": "weightlifting for 90 minutes"
        },
        "bundle_stats": {...},
        "preferences": {
            "soft_preferences": ["sweet flavor", "high-protein"],  // Auto-added
            "hard_filters": []
        },
        "key_principles": [
            {"principle": "Prioritize protein intake for muscle recovery"},
            {"principle": "Include complex carbohydrates for sustained energy"}
        ],
        "reasoning": "...Added high-protein preference based on strength activity detection..."
    }
    """)


def print_frontend_display_example():
    """Show how the frontend would display the information."""
    print("\n" + "="*60)
    print("FRONTEND DISPLAY EXAMPLE")
    print("="*60)
    
    print("""
    Based on your profile:
    25 years old, 70kg, cardio for 60 minutes, these are your macro targets: 
    25g protein, 75g carbs, 15g fat, 1000mg electrolytes
    
    What this bundle provides:
    28.5g protein, 78.2g carbs, 16.8g fat, 120mg electrolytes, 485 calories
    
    Selected 6 snacks with 85.2% target match.
    
    These snacks are tagged: sweet flavor, fruity flavor, crunchy texture, vegan, no nuts
    
    Some key principles:
    - Focus on easily digestible carbohydrates before cardio
    - Include moderate protein for muscle preservation
    
    RECOMMENDED SNACKS:
    1. Product Name
       Protein: 10g | Carbs: 25g | Fat: 5g | Calories: 165
       [Product Image] [Buy Now]
    
    2. Another Product
       Protein: 8g | Carbs: 30g | Fat: 3g | Calories: 180
       [Product Image] [Buy Now]
    
    ... (more products)
    """)


if __name__ == "__main__":
    asyncio.run(demonstrate_enhanced_response())
    print_frontend_display_example() 