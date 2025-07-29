#!/usr/bin/env python3
"""
Test script for the enhanced embedding system.

This script demonstrates how the enhanced embedding system works for matching
user queries with soft preferences and macro targets to product schemas.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.enhanced_embedding import (
    generate_user_query_embedding_text,
    generate_user_query_embedding,
    generate_enhanced_product_embedding_text,
    generate_enhanced_product_embedding,
    rank_products_by_similarity,
    get_top_matching_products,
    debug_embedding_matching
)
from app.db.session import SessionLocal
from app.db.models import Product

def test_enhanced_embedding_system():
    """Test the enhanced embedding system with sample data."""
    
    print("=== Enhanced Embedding System Test ===\n")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get some sample products
        products = db.query(Product).limit(5).all()
        
        if not products:
            print("No products found in database. Please add some products first.")
            return
        
        print(f"Testing with {len(products)} products:")
        for i, product in enumerate(products):
            print(f"  {i+1}. {product.name} ({product.brand})")
        print()
        
        # Test 1: Basic user query without preferences
        print("=== Test 1: Basic User Query ===")
        user_query = "I need a protein bar for post-workout recovery"
        
        print(f"User Query: {user_query}")
        
        # Generate user embedding text
        user_embedding_text = generate_user_query_embedding_text(user_query)
        print(f"User Embedding Text: {user_embedding_text}")
        
        # Rank products
        ranked_products = rank_products_by_similarity(user_query, products)
        
        print("\nTop 3 matches:")
        for i, (product, score) in enumerate(ranked_products[:3]):
            print(f"  {i+1}. {product.name} (Score: {score:.3f})")
        
        # Test 2: User query with soft preferences
        print("\n=== Test 2: User Query with Soft Preferences ===")
        user_query_2 = "I want a chocolate flavored chewy snack"
        soft_preferences = {
            "flavor": ["chocolate"],
            "texture": ["chewy"],
            "price_dollars": None
        }
        
        print(f"User Query: {user_query_2}")
        print(f"Soft Preferences: {soft_preferences}")
        
        user_embedding_text_2 = generate_user_query_embedding_text(user_query_2, soft_preferences)
        print(f"User Embedding Text: {user_embedding_text_2}")
        
        # Rank products with soft preferences
        ranked_products_2 = rank_products_by_similarity(user_query_2, products, soft_preferences)
        
        print("\nTop 3 matches:")
        for i, (product, score) in enumerate(ranked_products_2[:3]):
            print(f"  {i+1}. {product.name} (Score: {score:.3f})")
        
        # Test 3: User query with macro targets
        print("\n=== Test 3: User Query with Macro Targets ===")
        user_query_3 = "I need a high-protein snack for muscle building"
        macro_targets = {
            "target_protein": 25.0,
            "target_carbs": 15.0,
            "target_calories": 200.0
        }
        
        print(f"User Query: {user_query_3}")
        print(f"Macro Targets: {macro_targets}")
        
        user_embedding_text_3 = generate_user_query_embedding_text(user_query_3, None, macro_targets)
        print(f"User Embedding Text: {user_embedding_text_3}")
        
        # Rank products with macro targets
        ranked_products_3 = rank_products_by_similarity(user_query_3, products, None, macro_targets)
        
        print("\nTop 3 matches:")
        for i, (product, score) in enumerate(ranked_products_3[:3]):
            print(f"  {i+1}. {product.name} (Score: {score:.3f})")
        
        # Test 4: Debug embedding matching
        print("\n=== Test 4: Debug Embedding Matching ===")
        test_product = products[0]
        debug_info = debug_embedding_matching(
            user_query="I want a sweet protein bar",
            product=test_product,
            soft_preferences={"flavor": ["sweet"], "texture": ["chewy"]},
            macro_targets={"target_protein": 20.0}
        )
        
        print(f"Debug Info:")
        print(f"  User Query: {debug_info['user_query']}")
        print(f"  User Embedding Text: {debug_info['user_embedding_text']}")
        print(f"  Product: {debug_info['product_name']}")
        print(f"  Product Embedding Text: {debug_info['product_embedding_text']}")
        print(f"  Similarity Score: {debug_info['similarity_score']:.3f}")
        
        print("\n=== Enhanced Embedding System Test Complete ===")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_enhanced_embedding_system()
