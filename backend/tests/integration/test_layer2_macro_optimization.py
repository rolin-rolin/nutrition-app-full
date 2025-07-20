#!/usr/bin/env python3
"""
Test Layer 2 macro optimization algorithms with various nutritional target scenarios.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product
from app.core.layer2_macro_optimization import optimize_macro_combination, MacroTargets

def test_layer2_macro_optimization():
    print("=== Layer 2 Macro Optimization Testing ===\n")
    db = SessionLocal()
    try:
        # Get all products
        products = db.query(Product).all()
        print(f"Loaded {len(products)} products from DB.")
        # Test scenarios
        scenarios = [
            {"name": "High Protein", "targets": MacroTargets(20, 10, 5, 100)},
            {"name": "High Carbs", "targets": MacroTargets(5, 30, 5, 100)},
            {"name": "Balanced", "targets": MacroTargets(10, 20, 10, 100)},
            {"name": "Low Fat", "targets": MacroTargets(10, 20, 2, 100)},
        ]
        for scenario in scenarios:
            print(f"\n--- {scenario['name']} ---")
            result = optimize_macro_combination(
                products=products,
                macro_targets=scenario["targets"],
                min_snacks=4,
                max_snacks=8,
                max_candidates=10,
                score_threshold=1.5
            )
            if result:
                print(f"Selected {len(result.products)} snacks with score {result.score:.3f}.")
                for i, p in enumerate(result.products):
                    print(f"  {i+1}. {p.name} | Protein: {p.protein}g | Carbs: {p.carbs}g | Fat: {p.fat}g | Calories: {p.calories}")
            else:
                print("No valid combination found.")
    finally:
        db.close()

if __name__ == "__main__":
    test_layer2_macro_optimization() 