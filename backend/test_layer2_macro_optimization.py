#!/usr/bin/env python3
"""
Test script for Layer 2: Macro Optimization

This script demonstrates the different algorithms for finding optimal
2-5 snack combinations that match nutritional targets.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product, MacroTarget
from app.core.layer2_macro_optimization import optimize_macro_combination, MacroTargets

def test_layer2_macro_optimization():
    """Test Layer 2 macro optimization with different scenarios."""
    
    print("=== Layer 2: Macro Optimization Testing ===\n")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get all products
        products = db.query(Product).all()
        print(f"Testing with {len(products)} products from database")
        
        # Test scenarios
        test_scenarios = [
            {
                "name": "High Protein Pre-Workout",
                "targets": MacroTargets(
                    target_protein_g=25.0,
                    target_carbs_g=30.0,
                    target_fat_g=5.0,
                    target_electrolytes_mg=200.0
                )
            },
            {
                "name": "Low Carb Post-Workout",
                "targets": MacroTargets(
                    target_protein_g=20.0,
                    target_carbs_g=15.0,
                    target_fat_g=10.0,
                    target_electrolytes_mg=300.0
                )
            },
            {
                "name": "Balanced Recovery",
                "targets": MacroTargets(
                    target_protein_g=15.0,
                    target_carbs_g=40.0,
                    target_fat_g=8.0,
                    target_electrolytes_mg=150.0
                )
            },
            {
                "name": "Electrolyte Focus",
                "targets": MacroTargets(
                    target_protein_g=10.0,
                    target_carbs_g=20.0,
                    target_fat_g=5.0,
                    target_electrolytes_mg=500.0
                )
            }
        ]
        
        # Test different algorithms
        algorithms = ["greedy", "dynamic_programming", "hybrid"]
        
        for scenario in test_scenarios:
            print(f"\n--- Scenario: {scenario['name']} ---")
            print(f"Targets: {scenario['targets'].target_protein_g}g protein, "
                  f"{scenario['targets'].target_carbs_g}g carbs, "
                  f"{scenario['targets'].target_fat_g}g fat, "
                  f"{scenario['targets'].target_electrolytes_mg}mg electrolytes")
            
            for algorithm in algorithms:
                print(f"\n  Algorithm: {algorithm}")
                
                try:
                    # Create a MacroTarget object for compatibility
                    macro_target = MacroTarget(
                        target_protein=scenario['targets'].target_protein_g,
                        target_carbs=scenario['targets'].target_carbs_g,
                        target_fat=scenario['targets'].target_fat_g,
                        target_electrolytes=scenario['targets'].target_electrolytes_mg
                    )
                    
                    # Run optimization
                    result = optimize_macro_combination(
                        products=products,
                        macro_targets=macro_target,
                        min_snacks=4,
                        max_snacks=10,
                        algorithm=algorithm
                    )
                    
                    if result:
                        print(f"    Selected {len(result.products)} snacks:")
                        for i, product in enumerate(result.products):
                            print(f"      {i+1}. {product.name} "
                                  f"({product.protein}g protein, {product.carbs}g carbs, "
                                  f"{product.fat}g fat, {product.electrolytes_mg}mg electrolytes)")
                        
                        print(f"    Totals: {result.total_protein:.1f}g protein, "
                              f"{result.total_carbs:.1f}g carbs, {result.total_fat:.1f}g fat, "
                              f"{result.total_electrolytes:.0f}mg electrolytes, "
                              f"{result.total_calories:.0f} calories")
                        print(f"    Score: {result.score:.3f}")
                        print(f"    Target Match: {result.target_match_percentage:.1f}%")
                        print(f"    Algorithm Used: {result.algorithm_used}")
                    else:
                        print("    No valid combination found")
                        
                except Exception as e:
                    print(f"    Error: {e}")
        
        # Test edge cases
        print(f"\n--- Edge Cases ---")
        
        # Test with very few products
        few_products = products[:3]
        print(f"\n  Few Products Test ({len(few_products)} products):")
        macro_target = MacroTarget(
            target_protein=20.0,
            target_carbs=30.0,
            target_fat=10.0,
            target_electrolytes=200.0
        )
        
        result = optimize_macro_combination(
            products=few_products,
            macro_targets=macro_target,
            min_snacks=4,
            max_snacks=5,
            algorithm="dynamic_programming"
        )
        
        if result:
            print(f"    Selected {len(result.products)} snacks:")
            for product in result.products:
                print(f"      - {product.name}")
            print(f"    Score: {result.score:.3f}")
        
        # Test with zero targets
        print(f"\n  Zero Targets Test:")
        macro_target = MacroTarget(
            target_protein=0.0,
            target_carbs=0.0,
            target_fat=0.0,
            target_electrolytes=0.0
        )
        
        result = optimize_macro_combination(
            products=products[:10],
            macro_targets=macro_target,
            min_snacks=4,
            max_snacks=6,
            algorithm="dynamic_programming"
        )
        
        if result:
            print(f"    Selected {len(result.products)} snacks (minimal targets):")
            for product in result.products:
                print(f"      - {product.name}")
            print(f"    Score: {result.score:.3f}")
        
    except Exception as e:
        print(f"Error testing Layer 2: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_layer2_macro_optimization() 