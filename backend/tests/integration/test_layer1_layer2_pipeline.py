#!/usr/bin/env python3
"""
Test the complete Layer 1 + Layer 2 pipeline

This script tests the full flow from vector search (Layer 1) to macro optimization (Layer 2).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product, MacroTarget
from app.db.vector_store import get_product_vector_store
from app.core.layer2_macro_optimization import optimize_macro_combination, MacroTargets

def test_layer1_layer2_pipeline():
    """Test the complete Layer 1 + Layer 2 pipeline."""
    
    print("=== Layer 1 + Layer 2 Pipeline Testing ===\n")
    
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
        
        # Layer 2: Macro optimization
        targets = MacroTargets(target_protein_g=20, target_carbs_g=30, target_fat_g=10, target_electrolytes_mg=200)
        optimization_result = optimize_macro_combination(
            products=candidate_products,
            macro_targets=targets,
            min_snacks=4,
            max_snacks=8,
            max_candidates=10,
            score_threshold=1.5
        )
        if optimization_result:
            print(f"Layer 2 selected {len(optimization_result.products)} snacks with score {optimization_result.score:.3f}.")
            for i, p in enumerate(optimization_result.products):
                print(f"  {i+1}. {p.name} | Protein: {p.protein}g | Carbs: {p.carbs}g | Fat: {p.fat}g | Calories: {p.calories}")
        else:
            print("No valid combination found.")
    finally:
        db.close()

if __name__ == "__main__":
    test_layer1_layer2_pipeline() 