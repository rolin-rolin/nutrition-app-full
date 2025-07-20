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
        query = "high protein pre-workout snack with carbs for energy"
        targets = MacroTarget(
            target_protein=25.0,
            target_carbs=40.0,
            target_fat=8.0,
            target_electrolytes=300.0
        )
        
        print(f"Query: '{query}'")
        print(f"Targets: {targets.target_protein}g protein, {targets.target_carbs}g carbs, "
              f"{targets.target_fat}g fat, {targets.target_electrolytes}mg electrolytes")
        print(f"Running optimization 5 times with different random seeds...\n")
        
        # Layer 1: Vector Search (same each time)
        vector_results = vector_store.query_similar_products(
            query=query,
            top_k=20,
            hard_filters=None,
            use_mmr=True,
            mmr_lambda=0.8
        )
        
        # Convert to Product objects
        candidate_products = []
        for result in vector_results:
            product = db.query(Product).filter(Product.id == result['product_id']).first()
            if product:
                candidate_products.append(product)
        
        print(f"Layer 1: Found {len(candidate_products)} candidate products")
        print(f"Top 5 candidates:")
        for i, product in enumerate(candidate_products[:5]):
            print(f"  {i+1}. {product.name} (score: {vector_results[i]['score']:.3f})")
        print()
        
        # Run Layer 2 multiple times
        results = []
        for run in range(5):
            print(f"--- Run {run + 1} ---")
            
            optimization_result = optimize_macro_combination(
                products=candidate_products,
                macro_targets=targets,
                min_snacks=4,
                max_snacks=8,
                max_candidates=10,
                score_threshold=1.5
            )
            
            if optimization_result:
                print(f"Selected {len(optimization_result.products)} snacks:")
                for i, product in enumerate(optimization_result.products):
                    print(f"  {i+1}. {product.name}")
                
                print(f"Totals: {optimization_result.total_protein:.1f}g protein, "
                      f"{optimization_result.total_carbs:.1f}g carbs, "
                      f"{optimization_result.total_fat:.1f}g fat, "
                      f"{optimization_result.total_electrolytes:.0f}mg electrolytes")
                print(f"Score: {optimization_result.score:.3f}, "
                      f"Target Match: {optimization_result.target_match_percentage:.1f}%")
                
                # Store for comparison
                results.append({
                    'run': run + 1,
                    'products': [p.name for p in optimization_result.products],
                    'score': optimization_result.score,
                    'target_match': optimization_result.target_match_percentage
                })
            else:
                print("No valid combination found")
            
            print()
        
        # Analyze results
        print("=== Analysis ===")
        print(f"Total runs: {len(results)}")
        
        if results:
            # Check for variety in results
            unique_combinations = set()
            for result in results:
                # Sort product names for consistent comparison
                combination_key = tuple(sorted(result['products']))
                unique_combinations.add(combination_key)
            
            print(f"Unique combinations found: {len(unique_combinations)}")
            print(f"Variety percentage: {(len(unique_combinations) / len(results)) * 100:.1f}%")
            
            # Show score distribution
            scores = [r['score'] for r in results]
            target_matches = [r['target_match'] for r in results]
            
            print(f"Score range: {min(scores):.3f} - {max(scores):.3f}")
            print(f"Target match range: {min(target_matches):.1f}% - {max(target_matches):.1f}%")
            
            # Show all unique combinations
            print(f"\nAll unique combinations:")
            for i, combination in enumerate(sorted(unique_combinations)):
                print(f"  {i+1}. {', '.join(combination)}")
        
        print(f"\n=== Randomization Test Complete ===")
        
    except Exception as e:
        print(f"Error testing randomization: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_randomization() 