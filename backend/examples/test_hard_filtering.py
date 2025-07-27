#!/usr/bin/env python3
"""
Test script for hard filtering in the recommendation pipeline.

This script tests that hard filters extracted by the LLM are properly applied
to pre-filter products before vector similarity search.
"""

import os
import sys
from pathlib import Path

# Add the backend app to the Python path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from dotenv import load_dotenv
from app.core.recommendation import _build_hard_filters_from_llm_extraction, _pre_filter_products_by_hard_constraints
from app.schemas.recommendation import RecommendationRequest
from app.db.session import SessionLocal
from app.db.models import Product

load_dotenv()

def test_hard_filter_extraction():
    """Test that hard filters are correctly extracted from LLM preferences."""
    
    print("=== Testing Hard Filter Extraction ===\n")
    
    # Test case 1: Complete LLM extraction
    preferences_1 = {
        "hard_filters": {
            "dietary": ["vegan", "gluten-free"],
            "allergens": ["milk", "nuts"]
        },
        "soft_preferences": {
            "flavor": ["sweet"],
            "texture": ["crunchy"],
            "price_dollars": 5.0
        }
    }
    
    hard_filters_1 = _build_hard_filters_from_llm_extraction(preferences_1)
    print("Test Case 1 - Complete LLM extraction:")
    print(f"Input preferences: {preferences_1}")
    print(f"Extracted hard filters: {hard_filters_1}")
    print()
    
    # Test case 2: Only dietary restrictions
    preferences_2 = {
        "hard_filters": {
            "dietary": ["keto"],
            "allergens": []
        }
    }
    
    hard_filters_2 = _build_hard_filters_from_llm_extraction(preferences_2)
    print("Test Case 2 - Only dietary restrictions:")
    print(f"Input preferences: {preferences_2}")
    print(f"Extracted hard filters: {hard_filters_2}")
    print()
    
    # Test case 3: Only allergens
    preferences_3 = {
        "hard_filters": {
            "dietary": [],
            "allergens": ["soy", "eggs"]
        }
    }
    
    hard_filters_3 = _build_hard_filters_from_llm_extraction(preferences_3)
    print("Test Case 3 - Only allergens:")
    print(f"Input preferences: {preferences_3}")
    print(f"Extracted hard filters: {hard_filters_3}")
    print()
    
    # Test case 4: Empty preferences
    preferences_4 = {}
    
    hard_filters_4 = _build_hard_filters_from_llm_extraction(preferences_4)
    print("Test Case 4 - Empty preferences:")
    print(f"Input preferences: {preferences_4}")
    print(f"Extracted hard filters: {hard_filters_4}")
    print()

def test_hard_filter_application():
    """Test that hard filters are correctly applied to filter products."""
    
    print("=== Testing Hard Filter Application ===\n")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Get total product count
        total_products = db.query(Product).count()
        print(f"Total products in database: {total_products}")
        
        # Test case 1: Vegan filter
        hard_filters_1 = {
            "dietary_requirements": ["vegan"]
        }
        
        filtered_products_1 = _pre_filter_products_by_hard_constraints(db, hard_filters_1)
        print(f"Test Case 1 - Vegan filter:")
        print(f"Hard filters: {hard_filters_1}")
        print(f"Products after filtering: {len(filtered_products_1)}")
        print(f"Reduction: {total_products - len(filtered_products_1)} products filtered out")
        
        # Show some examples
        if filtered_products_1:
            print("Sample vegan products:")
            for i, product in enumerate(filtered_products_1[:3]):
                print(f"  {i+1}. {product.name} (dietary_flags: {product.dietary_flags}, diet: {product.diet})")
        print()
        
        # Test case 2: Gluten-free filter
        hard_filters_2 = {
            "dietary_requirements": ["gluten-free"]
        }
        
        filtered_products_2 = _pre_filter_products_by_hard_constraints(db, hard_filters_2)
        print(f"Test Case 2 - Gluten-free filter:")
        print(f"Hard filters: {hard_filters_2}")
        print(f"Products after filtering: {len(filtered_products_2)}")
        print(f"Reduction: {total_products - len(filtered_products_2)} products filtered out")
        
        # Show some examples
        if filtered_products_2:
            print("Sample gluten-free products:")
            for i, product in enumerate(filtered_products_2[:3]):
                print(f"  {i+1}. {product.name} (dietary_flags: {product.dietary_flags}, diet: {product.diet})")
        print()
        
        # Test case 3: Allergen filter (exclude milk)
        hard_filters_3 = {
            "allergen_restrictions": ["milk"]
        }
        
        filtered_products_3 = _pre_filter_products_by_hard_constraints(db, hard_filters_3)
        print(f"Test Case 3 - Exclude milk allergen:")
        print(f"Hard filters: {hard_filters_3}")
        print(f"Products after filtering: {len(filtered_products_3)}")
        print(f"Reduction: {total_products - len(filtered_products_3)} products filtered out")
        
        # Show some examples
        if filtered_products_3:
            print("Sample products without milk:")
            for i, product in enumerate(filtered_products_3[:3]):
                print(f"  {i+1}. {product.name} (allergens: {product.allergens})")
        print()
        
        # Test case 4: Combined filters (vegan + no nuts)
        hard_filters_4 = {
            "dietary_requirements": ["vegan"],
            "allergen_restrictions": ["tree-nuts"]
        }
        
        filtered_products_4 = _pre_filter_products_by_hard_constraints(db, hard_filters_4)
        print(f"Test Case 4 - Vegan + no tree nuts:")
        print(f"Hard filters: {hard_filters_4}")
        print(f"Products after filtering: {len(filtered_products_4)}")
        print(f"Reduction: {total_products - len(filtered_products_4)} products filtered out")
        
        # Show some examples
        if filtered_products_4:
            print("Sample vegan products without tree nuts:")
            for i, product in enumerate(filtered_products_4[:3]):
                print(f"  {i+1}. {product.name} (dietary_flags: {product.dietary_flags}, allergens: {product.allergens})")
        print()
        
    except Exception as e:
        print(f"Error in hard filter application test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

def test_full_recommendation_flow():
    """Test the full recommendation flow with LLM-extracted hard filters."""
    
    print("=== Testing Full Recommendation Flow ===\n")
    
    # Test case: User query with LLM-extracted preferences
    request = RecommendationRequest(
        user_query="I'm a 25-year-old vegan who's allergic to nuts. I want sweet, crunchy snacks for my 45-minute gym workout. Budget is $5.",
        age=25,
        weight_kg=70.0,
        exercise_type="strength",
        exercise_duration_minutes=45,
        preferences={
            "hard_filters": {
                "dietary": ["vegan"],
                "allergens": ["tree-nuts"]
            },
            "soft_preferences": {
                "flavor": ["sweet"],
                "texture": ["crunchy"],
                "price_dollars": 5.0
            },
            "calorie_cap": 300
        }
    )
    
    print("Test Case - Full recommendation request:")
    print(f"User query: {request.user_query}")
    print(f"Age: {request.age}, Weight: {request.weight_kg}kg")
    print(f"Exercise: {request.exercise_type} for {request.exercise_duration_minutes} minutes")
    print(f"Preferences: {request.preferences}")
    print()
    
    # Extract hard filters
    hard_filters = _build_hard_filters_from_llm_extraction(request.preferences or {})
    print(f"Extracted hard filters: {hard_filters}")
    print()
    
    # Apply hard filters to products
    db = SessionLocal()
    try:
        pre_filtered_products = _pre_filter_products_by_hard_constraints(db, hard_filters)
        print(f"Pre-filtered products: {len(pre_filtered_products)} out of {db.query(Product).count()} total")
        
        if pre_filtered_products:
            print("Sample pre-filtered products:")
            for i, product in enumerate(pre_filtered_products[:5]):
                print(f"  {i+1}. {product.name}")
                print(f"     - Dietary flags: {product.dietary_flags}")
                print(f"     - Allergens: {product.allergens}")
                print(f"     - Price: ${product.price_usd}")
                print()
        
    except Exception as e:
        print(f"Error in full flow test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Hard Filtering Test Suite")
    print("=======================\n")
    
    # Test hard filter extraction
    test_hard_filter_extraction()
    
    # Test hard filter application
    test_hard_filter_application()
    
    # Test full recommendation flow
    test_full_recommendation_flow()
    
    print("\nTest completed!") 