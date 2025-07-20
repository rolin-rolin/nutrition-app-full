#!/usr/bin/env python3
"""
Test script for Layer 1 vector search.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product
from app.db.vector_store import get_product_vector_store

def test_vector_search():
    print("=== Layer 1 Vector Search Testing ===\n")
    db = SessionLocal()
    try:
        vector_store = get_product_vector_store()
        query = "protein bar"
        print(f"Query: {query}")
        results = vector_store.query_similar_products(query=query, top_k=10)
        for i, r in enumerate(results):
            product = db.query(Product).filter(Product.id == r['product_id']).first()
            if product:
                print(f"{i+1}. {product.name} | Score: {r['score']:.3f}")
    finally:
        db.close()

if __name__ == "__main__":
    test_vector_search() 