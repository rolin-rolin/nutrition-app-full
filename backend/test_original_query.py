#!/usr/bin/env python3
"""
Test the original problematic query to see what's happening.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.vector_store import get_product_vector_store
from app.db.models import Product

def test_original_query():
    """Test the original problematic query."""
    
    print("=== Testing Original Query ===\n")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get vector store
        vector_store = get_product_vector_store()
        
        # The original problematic query
        original_query = "protein bar with nuts for pre-workout"
        
        print(f"Original query: '{original_query}'")
        
        # Test with different settings
        print("\n--- Without MMR (raw similarity) ---")
        results = vector_store.query_similar_products(
            query=original_query,
            top_k=10,
            hard_filters=None,
            use_mmr=False
        )
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results):
            product = db.query(Product).filter(Product.id == result['product_id']).first()
            if product:
                print(f"  {i+1}. {product.name} (score: {result['score']:.3f})")
                if i < 3:  # Show details for top 3
                    print(f"      Categories: {product.categories}")
                    print(f"      Tags: {product.tags}")
                    print(f"      Description: {product.description[:100]}...")
        
        print("\n--- With MMR (diversity) ---")
        results_mmr = vector_store.query_similar_products(
            query=original_query,
            top_k=10,
            hard_filters=None,
            use_mmr=True,
            mmr_lambda=0.5
        )
        
        print(f"Found {len(results_mmr)} results:")
        for i, result in enumerate(results_mmr):
            product = db.query(Product).filter(Product.id == result['product_id']).first()
            if product:
                print(f"  {i+1}. {product.name} (score: {result['score']:.3f})")
                if i < 3:  # Show details for top 3
                    print(f"      Categories: {product.categories}")
                    print(f"      Tags: {product.tags}")
                    print(f"      Description: {product.description[:100]}...")
        
        # Check if protein bar is in top 5
        protein_bar_in_top5 = any(
            db.query(Product).filter(Product.id == result['product_id']).first().name == "Protein Bar - Chocolate"
            for result in results[:5]
        )
        
        print(f"\n--- Analysis ---")
        print(f"Protein Bar in top 5 without MMR: {protein_bar_in_top5}")
        print(f"Protein Bar in top 5 with MMR: {any(db.query(Product).filter(Product.id == result['product_id']).first().name == 'Protein Bar - Chocolate' for result in results_mmr[:5])}")
        
    except Exception as e:
        print(f"Error testing original query: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_original_query() 