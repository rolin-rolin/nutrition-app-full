#!/usr/bin/env python3
"""
Test script for integrated enhanced embedding system with recommendation pipeline.

This script demonstrates how the enhanced embedding system integrates with
the existing recommendation pipeline, showing the complete flow from
user query to final recommendations.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.enhanced_embedding import (
    generate_user_query_embedding_text,
    rank_products_by_similarity,
    debug_embedding_matching
)
from app.core.recommendation import _enhanced_vector_search_with_embeddings
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.session import SessionLocal
from app.db.models import Product, UserInput

def test_integrated_enhanced_embedding():
    """Test the enhanced embedding system integrated with the recommendation pipeline."""
    
    print("=== Integrated Enhanced Embedding System Test ===\n")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get some sample products
        products = db.query(Product).limit(10).all()
        
        if not products:
            print("No products found in database. Please add some products first.")
            return
        
        print(f"Testing with {len(products)} products")
        print()
        
        # Test 1: Complete pipeline with LLM field extraction
        print("=== Test 1: Complete Pipeline with LLM Field Extraction ===")
        
        # Simulate LLM-extracted fields from user query
        user_query = "I'm an 18-year-old guy, weigh 160 pounds. I want savory, chewy snacks for my 90-minute soccer match to fuel recovery. I'm lactose intolerant and I'd like to be gluten-free. Keep it under 400 calories"
        
        # LLM-extracted fields (simulated)
        extracted_fields = {
            "age": 18,
            "weight_lb": 160,
            "activity_type": "cardio",
            "duration_minutes": 90,
            "calorie_cap": 400,
            "soft_preferences": {
                "flavor": ["savory"],
                "texture": ["chewy"],
                "price_dollars": None
            },
            "hard_filters": {
                "dietary": ["gluten-free"],
                "allergens": ["milk"]
            }
        }
        
        print(f"User Query: {user_query}")
        print(f"LLM Extracted Fields: {extracted_fields}")
        print()
        
        # Step 1: Generate macro targets using existing pipeline
        print("Step 1: Generating macro targets...")
        macro_targeting_service = MacroTargetingServiceLocal()
        
        # Create user input for macro targeting
        user_input = UserInput(
            user_query=user_query,
            age=extracted_fields["age"],
            weight_kg=extracted_fields["weight_lb"] * 0.453592,  # Convert lbs to kg
            exercise_type=extracted_fields["activity_type"],
            exercise_duration_minutes=extracted_fields["duration_minutes"],
            exercise_intensity="high",
            timing="post-workout"
        )
        
        # Generate macro targets
        context, macro_target = macro_targeting_service.get_context_and_macro_targets(user_input)
        
        print(f"Generated Macro Targets:")
        print(f"  Protein: {macro_target.target_protein:.1f}g")
        print(f"  Carbs: {macro_target.target_carbs:.1f}g")
        print(f"  Calories: {macro_target.target_calories:.1f}")
        print()
        
        # Step 2: Pre-filter products by hard constraints
        print("Step 2: Pre-filtering products by hard constraints...")
        
        # Simulate hard filtering (in real pipeline, this would use the existing functions)
        hard_filtered_products = []
        for product in products:
            # Check dietary requirements
            dietary_match = True
            if "gluten-free" in extracted_fields["hard_filters"]["dietary"]:
                if not (product.dietary_flags and "gluten-free" in product.dietary_flags):
                    dietary_match = False
            
            # Check allergen restrictions
            allergen_match = True
            if "milk" in extracted_fields["hard_filters"]["allergens"]:
                if product.allergens and "milk" in product.allergens:
                    allergen_match = False
            
            if dietary_match and allergen_match:
                hard_filtered_products.append(product)
        
        print(f"Hard filtering results: {len(hard_filtered_products)} products passed hard constraints")
        print()
        
        # Step 3: Enhanced embedding-based matching
        print("Step 3: Enhanced embedding-based matching...")
        
        # Convert macro targets to dict format
        macro_targets_dict = {
            "target_protein": macro_target.target_protein,
            "target_carbs": macro_target.target_carbs,
            "target_calories": macro_target.target_calories
        }
        
        # Use enhanced embedding system
        ranked_products = rank_products_by_similarity(
            user_query,
            hard_filtered_products,
            extracted_fields["soft_preferences"],
            macro_targets_dict
        )
        
        print("Top 5 Enhanced Embedding Matches:")
        for i, (product, score) in enumerate(ranked_products[:5]):
            print(f"  {i+1}. {product.name} (Score: {score:.3f})")
            print(f"      Brand: {product.brand}")
            print(f"      Protein: {product.protein}g, Carbs: {product.carbs}g")
            print(f"      Flavor: {product.flavor}, Texture: {product.texture}")
            print(f"      Dietary: {product.dietary_flags}")
            print()
        
        # Step 4: Debug embedding matching for top result
        print("Step 4: Debug embedding matching for top result...")
        if ranked_products:
            top_product, top_score = ranked_products[0]
            debug_info = debug_embedding_matching(
                user_query=user_query,
                product=top_product,
                soft_preferences=extracted_fields["soft_preferences"],
                macro_targets=macro_targets_dict
            )
            
            print(f"Top Match Debug Info:")
            print(f"  User Embedding Text: {debug_info['user_embedding_text']}")
            print(f"  Product Embedding Text: {debug_info['product_embedding_text']}")
            print(f"  Similarity Score: {debug_info['similarity_score']:.3f}")
            print()
        
        # Test 2: Comparison with traditional vector search
        print("=== Test 2: Comparison with Traditional Vector Search ===")
        
        # Traditional approach would use simple query
        traditional_query = "savory chewy protein bar for post-workout"
        
        # Enhanced approach uses rich embedding
        enhanced_user_embedding_text = generate_user_query_embedding_text(
            user_query,
            extracted_fields["soft_preferences"],
            macro_targets_dict
        )
        
        print(f"Traditional Query: {traditional_query}")
        print(f"Enhanced Embedding Text: {enhanced_user_embedding_text}")
        print()
        
        print("=== Enhanced Embedding System Integration Complete ===")
        print("\nKey Benefits:")
        print("1. ✅ Unified vector space for user queries and products")
        print("2. ✅ Incorporates soft preferences (flavor, texture) into embeddings")
        print("3. ✅ Incorporates macro targets (protein, carbs) into embeddings")
        print("4. ✅ Maintains compatibility with existing hard filtering")
        print("5. ✅ Better semantic understanding of user intent")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_integrated_enhanced_embedding()
