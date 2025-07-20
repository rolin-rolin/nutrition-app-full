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
        
        # Test scenarios with realistic queries and targets
        test_scenarios = [
            {
                "name": "Pre-Workout Energy Boost",
                "query": "high protein pre-workout snack with carbs for energy",
                "targets": MacroTargets(
                    target_protein_g=25.0,
                    target_carbs_g=40.0,
                    target_fat_g=8.0,
                    target_electrolytes_mg=300.0
                )
            },
            {
                "name": "Post-Workout Recovery",
                "query": "protein and carbs for muscle recovery after workout",
                "targets": MacroTargets(
                    target_protein_g=30.0,
                    target_carbs_g=50.0,
                    target_fat_g=10.0,
                    target_electrolytes_mg=400.0
                )
            },
            {
                "name": "Low Carb Snack Pack",
                "query": "low carb high protein snacks for weight loss",
                "targets": MacroTargets(
                    target_protein_g=35.0,
                    target_carbs_g=20.0,
                    target_fat_g=15.0,
                    target_electrolytes_mg=250.0
                )
            },
            {
                "name": "Electrolyte Replenishment",
                "query": "electrolyte rich snacks for hydration",
                "targets": MacroTargets(
                    target_protein_g=15.0,
                    target_carbs_g=30.0,
                    target_fat_g=8.0,
                    target_electrolytes_mg=600.0
                )
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n--- Scenario: {scenario['name']} ---")
            print(f"Query: '{scenario['query']}'")
            print(f"Targets: {scenario['targets'].target_protein_g}g protein, "
                  f"{scenario['targets'].target_carbs_g}g carbs, "
                  f"{scenario['targets'].target_fat_g}g fat, "
                  f"{scenario['targets'].target_electrolytes_mg}mg electrolytes")
            
            # Layer 1: Vector Search
            print(f"\n  Layer 1: Vector Search")
            vector_results = vector_store.query_similar_products(
                query=scenario['query'],
                top_k=20,  # Get more candidates for Layer 2
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
            
            print(f"    Found {len(candidate_products)} candidate products from vector search")
            print(f"    Top 5 candidates:")
            for i, product in enumerate(candidate_products[:5]):
                print(f"      {i+1}. {product.name} (score: {vector_results[i]['score']:.3f})")
            
            # Layer 2: Macro Optimization
            print(f"\n  Layer 2: Macro Optimization")
            
            # Create MacroTarget object
            macro_target = MacroTarget(
                target_protein=scenario['targets'].target_protein_g,
                target_carbs=scenario['targets'].target_carbs_g,
                target_fat=scenario['targets'].target_fat_g,
                target_electrolytes=scenario['targets'].target_electrolytes_mg
            )
            
            # Run optimization with randomization
            optimization_result = optimize_macro_combination(
                products=candidate_products,
                macro_targets=macro_target,
                min_snacks=4,
                max_snacks=8,
                max_candidates=10,
                score_threshold=1.5
            )
            
            if optimization_result:
                print(f"    Selected {len(optimization_result.products)} snacks:")
                for i, product in enumerate(optimization_result.products):
                    print(f"      {i+1}. {product.name}")
                    print(f"         Protein: {product.protein}g, Carbs: {product.carbs}g, "
                          f"Fat: {product.fat}g, Electrolytes: {product.electrolytes_mg}mg")
                
                print(f"\n    Final Combination Totals:")
                print(f"      Protein: {optimization_result.total_protein:.1f}g "
                      f"(target: {scenario['targets'].target_protein_g}g)")
                print(f"      Carbs: {optimization_result.total_carbs:.1f}g "
                      f"(target: {scenario['targets'].target_carbs_g}g)")
                print(f"      Fat: {optimization_result.total_fat:.1f}g "
                      f"(target: {scenario['targets'].target_fat_g}g)")
                print(f"      Electrolytes: {optimization_result.total_electrolytes:.0f}mg "
                      f"(target: {scenario['targets'].target_electrolytes_mg}mg)")
                print(f"      Calories: {optimization_result.total_calories:.0f}")
                
                print(f"\n    Performance Metrics:")
                print(f"      Optimization Score: {optimization_result.score:.3f}")
                print(f"      Target Match: {optimization_result.target_match_percentage:.1f}%")
                print(f"      Algorithm Used: {optimization_result.algorithm_used}")
                
                # Calculate macro match percentages
                protein_match = min(100, (optimization_result.total_protein / scenario['targets'].target_protein_g) * 100) if scenario['targets'].target_protein_g > 0 else 100
                carbs_match = min(100, (optimization_result.total_carbs / scenario['targets'].target_carbs_g) * 100) if scenario['targets'].target_carbs_g > 0 else 100
                fat_match = min(100, (optimization_result.total_fat / scenario['targets'].target_fat_g) * 100) if scenario['targets'].target_fat_g > 0 else 100
                electrolytes_match = min(100, (optimization_result.total_electrolytes / scenario['targets'].target_electrolytes_mg) * 100) if scenario['targets'].target_electrolytes_mg > 0 else 100
                
                print(f"      Macro Matches: Protein {protein_match:.1f}%, Carbs {carbs_match:.1f}%, "
                      f"Fat {fat_match:.1f}%, Electrolytes {electrolytes_match:.1f}%")
            else:
                print("    No valid combination found")
            
            print(f"\n" + "="*60)
        
        # Test edge case: Very specific query with hard filters
        print(f"\n--- Edge Case: Vegan Pre-Workout ---")
        print(f"Query: 'vegan protein snack for pre-workout'")
        
        # Layer 1 with hard filter
        vegan_results = vector_store.query_similar_products(
            query="vegan protein snack for pre-workout",
            top_k=15,
            hard_filters={"dietary_flags": ["vegan"]},
            use_mmr=True,
            mmr_lambda=0.8
        )
        
        vegan_products = []
        for result in vegan_results:
            product = db.query(Product).filter(Product.id == result['product_id']).first()
            if product:
                vegan_products.append(product)
        
        print(f"  Layer 1: Found {len(vegan_products)} vegan products")
        
        if vegan_products:
            # Layer 2 optimization
            vegan_target = MacroTarget(
                target_protein=20.0,
                target_carbs=30.0,
                target_fat=8.0,
                target_electrolytes=200.0
            )
            
            vegan_optimization = optimize_macro_combination(
                products=vegan_products,
                macro_targets=vegan_target,
                min_snacks=4,
                max_snacks=6,
                max_candidates=10,
                score_threshold=1.5
            )
            
            if vegan_optimization:
                print(f"  Layer 2: Selected {len(vegan_optimization.products)} vegan snacks")
                for product in vegan_optimization.products:
                    print(f"    - {product.name}")
                print(f"    Score: {vegan_optimization.score:.3f}, "
                      f"Target Match: {vegan_optimization.target_match_percentage:.1f}%")
        
        print(f"\n=== Pipeline Test Complete ===")
        
    except Exception as e:
        print(f"Error testing pipeline: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_layer1_layer2_pipeline() 