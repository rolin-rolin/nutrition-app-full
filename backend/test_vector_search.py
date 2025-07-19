#!/usr/bin/env python3
""" 
This script will test the Layer 1 vector search with sample queries.
"""


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.vector_store import get_product_vector_store
from app.db.models import Product

def test_vector_search():
    """Test vector search with sample queries."""

    print("Testing vector search functionality...")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get vector store
        vector_store = get_product_vector_store()
        
        # Test queries
        test_queries = [
            "I want a chewy chocolate vegan snack that's good for recovery",
            "protein bar with nuts for pre-workout",
            "low carb energy drink for during workout",
            "sweet smoothie for post-workout recovery"
        ]
        
        for query in test_queries:
            print(f"\n--- Testing query: '{query}' ---")
            
            # Test with no hard filters
            results = vector_store.query_similar_products(
                query=query,
                top_k=5,
                hard_filters=None,
                use_mmr=True,
                mmr_lambda=0.5
            )
            
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results[:3]):  # Show top3
                product = db.query(Product).filter(Product.id == result['product_id']).first()
                if product:
                    print(f"  {i+1}. {product.name} (score: {result['score']:.3f})")
            
            # Test with hard filters
            print("\n  With vegan filter:")
            vegan_results = vector_store.query_similar_products(
                query=query,
                top_k=5,
                hard_filters={"dietary_flags": ["vegan"]},
                use_mmr=True,
                mmr_lambda=0.5   
            )
            
            print(f"  Found {len(vegan_results)} vegan results:")
            for i, result in enumerate(vegan_results[:3]):
                product = db.query(Product).filter(Product.id == result['product_id']).first()
                if product:
                    print(f"    {i+1}. {product.name} (score: {result['score']:.3f})")
        
        print("\nVector search test completed!")
    except Exception as e:
        print(f"Error testing vector search: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_vector_search() 