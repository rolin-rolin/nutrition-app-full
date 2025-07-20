#!/usr/bin/env python3
"""
Test the randomization feature in Layer 2 macro optimization.

This script runs the same query multiple times to show that different
valid combinations are returned each time.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product, MacroTarget
from app.db.vector_store import get_product_vector_store
from app.core.layer2_macro_optimization import optimize_macro_combination

def test_randomization():
    """Test that the same query returns different results due to randomization."""
    
    print("=== Layer 2 Randomization Testing ===\n")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get vector store
        vector_store = get_product_vector_store()
        
        # Test scenario
        query = "high protein pre-workout snack"
        print(f"Query: {query}")
        
        # Layer 1: Vector search
        vector_results = vector_store.query_similar_products(query=query, top_k=20)
        candidate_products = [db.query(Product).filter(Product.id == r['product_id']).first() for r in vector_results]
        candidate_products = [p for p in candidate_products if p]
        print(f"Layer 1 returned {len(candidate_products)} products.")
        
        # Layer 2: Macro optimization (run multiple times)
        targets = MacroTarget(target_protein=20, target_carbs=30, target_fat=10, target_electrolytes=200)
        seen_combinations = set()
        for run in range(5):
            optimization_result = optimize_macro_combination(
                products=candidate_products,
                macro_targets=targets,
                min_snacks=4,
                max_snacks=8,
                max_candidates=10,
                score_threshold=1.5
            )
            if optimization_result:
                combo = tuple(sorted(p.id for p in optimization_result.products))
                seen_combinations.add(combo)
                print(f"Run {run+1}: Score {optimization_result.score:.3f}, Products: {[p.name for p in optimization_result.products]}")
            else:
                print(f"Run {run+1}: No valid combination found.")
        print(f"\nUnique combinations: {len(seen_combinations)} out of 5 runs.")
    finally:
        db.close()

if __name__ == "__main__":
    test_randomization() 