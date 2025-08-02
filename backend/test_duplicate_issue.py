#!/usr/bin/env python3
"""
Test for duplicate products in vector search
"""

import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product
from app.db.vector_store import get_product_vector_store

def test_duplicate_issue():
    """Test for duplicate products in vector search"""
    print("=== Testing Duplicate Products ===")
    
    db = SessionLocal()
    try:
        # Test 1: Check all products in database
        all_products = db.query(Product).all()
        print(f"Total products in database: {len(all_products)}")
        
        # Check for duplicate IDs
        product_ids = [p.id for p in all_products]
        unique_ids = set(product_ids)
        print(f"Unique product IDs: {len(unique_ids)}")
        
        if len(product_ids) != len(unique_ids):
            print("❌ DUPLICATE PRODUCT IDs IN DATABASE")
            from collections import Counter
            duplicates = [id for id, count in Counter(product_ids).items() if count > 1]
            print(f"Duplicate IDs: {duplicates}")
        else:
            print("✅ No duplicate product IDs in database")
        
        # Test 2: Check vector search for duplicates
        vector_store = get_product_vector_store()
        
        # Test different queries
        test_queries = [
            "avoid: ",
            "protein bar",
            "chocolate",
            "peanut butter"
        ]
        
        for query in test_queries:
            print(f"\n--- Testing query: '{query}' ---")
            
            vector_results = vector_store.query_similar_products(
                query=query,
                top_k=20,
                hard_filters=None,
                use_mmr=True,
                mmr_lambda=0.5
            )
            
            print(f"Vector search returned {len(vector_results)} results")
            
            # Check for duplicate product IDs
            result_ids = [result['product_id'] for result in vector_results]
            unique_result_ids = set(result_ids)
            
            print(f"Unique product IDs in results: {len(unique_result_ids)}")
            
            if len(result_ids) != len(unique_result_ids):
                print("❌ DUPLICATE PRODUCT IDs IN VECTOR SEARCH")
                from collections import Counter
                duplicates = [id for id, count in Counter(result_ids).items() if count > 1]
                print(f"Duplicate IDs: {duplicates}")
                
                # Show the duplicate products
                for dup_id in duplicates:
                    product = db.query(Product).filter(Product.id == dup_id).first()
                    if product:
                        print(f"  Duplicate: {product.name} (ID: {dup_id})")
            else:
                print("✅ No duplicate product IDs in vector search")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_duplicate_issue() 