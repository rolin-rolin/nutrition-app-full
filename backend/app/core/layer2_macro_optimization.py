#!/usr/bin/env python3
"""
Layer 2: Macro Optimization (Numeric Filtering)

This module implements dynamic programming to find optimal combinations of 4-10 snacks
that best match the user's nutritional targets with randomization for variety.

Algorithm:
- Dynamic Programming with Randomization - Finds multiple valid combinations and
  randomly selects one to provide variety while maintaining quality.
  Matches protein, carbs, fat, and electrolyte targets.
"""

import itertools
import math
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session
import numpy as np



from app.db.models import Product, MacroTarget

@dataclass
class MacroTargets:
    """Container for macro targets with validation."""
    target_protein_g: float = 0.0
    target_carbs_g: float = 0.0
    target_fat_g: float = 0.0
    target_electrolytes_mg: float = 0.0
    
    def __post_init__(self):
        """Validate that targets are non-negative."""
        for field in ['target_protein_g', 'target_carbs_g', 'target_fat_g', 'target_electrolytes_mg']:
            value = getattr(self, field)
            if value < 0:
                setattr(self, field, 0.0)

@dataclass
class CombinationResult:
    """Result of macro optimization."""
    products: List[Product]
    total_protein: float
    total_carbs: float
    total_fat: float
    total_electrolytes: float
    total_calories: float
    score: float
    algorithm_used: str
    target_match_percentage: float

class MacroOptimizer:
    """Advanced macro optimization engine for Layer 2."""
    
    def __init__(self, 
                 min_snacks: int = 4, 
                 max_snacks: int = 10,
                 protein_weight: float = 1.0,
                 carbs_weight: float = 1.0,
                 fat_weight: float = 1.0,
                 electrolytes_weight: float = 0.5):
        """
        Initialize the macro optimizer.
        
        Args:
            min_snacks: Minimum number of snacks in combination (4-10)
            max_snacks: Maximum number of snacks in combination (4-10)
            protein_weight: Weight for protein matching (higher = more important)
            carbs_weight: Weight for carbs matching
            fat_weight: Weight for fat matching
            electrolytes_weight: Weight for electrolytes matching
        """
        self.min_snacks = min_snacks
        self.max_snacks = max_snacks
        self.weights = {
            'protein': protein_weight,
            'carbs': carbs_weight,
            'fat': fat_weight,
            'electrolytes': electrolytes_weight
        }
    
    def calculate_combination_score(self, 
                                  products: List[Product], 
                                  targets: MacroTargets) -> Tuple[float, Dict[str, float]]:
        """
        Calculate how well a combination matches the macro targets.
        
        Returns:
            Tuple of (total_score, macro_totals)
        """
        if not products:
            return float('inf'), {}
        
        # Calculate totals
        totals = {
            'protein': sum(p.protein or 0 for p in products),
            'carbs': sum(p.carbs or 0 for p in products),
            'fat': sum(p.fat or 0 for p in products),
            'electrolytes': sum(p.electrolytes_mg or 0 for p in products),
            'calories': sum(p.calories or 0 for p in products)
        }
        
        # Calculate weighted percentage differences
        target_values = {
            'protein': targets.target_protein_g,
            'carbs': targets.target_carbs_g,
            'fat': targets.target_fat_g,
            'electrolytes': targets.target_electrolytes_mg
        }
        
        total_score = 0.0
        for macro, total in totals.items():
            if macro == 'calories':
                continue  # Calories handled separately
                
            target = target_values[macro]
            if target > 0:
                # Calculate percentage difference with asymmetric penalties
                if total < target:
                    # Penalize being under target more heavily
                    diff = (target - total) / target
                    weighted_diff = diff * self.weights[macro] * 1.5
                else:
                    # Be more lenient when exceeding target (common with 4-10 snacks)
                    diff = (total - target) / target
                    weighted_diff = diff * self.weights[macro] * 0.7
                total_score += weighted_diff
            elif total > 0:
                # Penalize if we have macros but no target
                total_score += self.weights[macro] * 0.5
        
        # Penalize too many or too few snacks
        snack_count_penalty = 0.0
        if len(products) < self.min_snacks:
            snack_count_penalty = (self.min_snacks - len(products)) * 0.2
        elif len(products) > self.max_snacks:
            snack_count_penalty = (len(products) - self.max_snacks) * 0.1
        
        total_score += snack_count_penalty
        
        return total_score, totals
    

    
    def dynamic_programming_algorithm(self, 
                                    products: List[Product], 
                                    targets: MacroTargets,
                                    max_candidates: int = 10,
                                    score_threshold: float = 0.3,
                                    calorie_cap: float = None) -> CombinationResult:
        """
        Dynamic programming algorithm that finds multiple valid combinations and randomly selects one.
        
        This works well for smaller datasets (up to ~20 products).
        
        Args:
            products: List of candidate products
            targets: Macro targets to match
            max_candidates: Maximum number of candidate combinations to keep
            score_threshold: Score threshold above which combinations are considered valid
            calorie_cap: If set, only consider combinations with total calories <= this value
        """
        if len(products) > 20:
            # Fall back to simple selection for large datasets
            return self._simple_selection_algorithm(products, targets)
        
        valid_combinations = []
        
        # Try all combinations of different sizes
        for size in range(self.min_snacks, min(self.max_snacks + 1, len(products) + 1)):
            for combination in itertools.combinations(products, size):
                score, totals = self.calculate_combination_score(list(combination), targets)
                
                # Enforce calorie cap if set
                if calorie_cap is not None and totals['calories'] > calorie_cap:
                    continue
                
                # Keep combinations that meet the score threshold
                if score <= score_threshold:
                    valid_combinations.append({
                        'combination': list(combination),
                        'score': score,
                        'totals': totals
                    })
        
        if not valid_combinations:
            # If no combinations meet the threshold, return the best one (below calorie cap if possible)
            best_combination = None
            best_score = float('inf')
            best_totals = {}
            
            for size in range(self.min_snacks, min(self.max_snacks + 1, len(products) + 1)):
                for combination in itertools.combinations(products, size):
                    score, totals = self.calculate_combination_score(list(combination), targets)
                    if calorie_cap is not None and totals['calories'] > calorie_cap:
                        continue
                    if score < best_score:
                        best_score = score
                        best_combination = list(combination)
                        best_totals = totals
            
            if not best_combination:
                return None
            
            target_match = self._calculate_target_match_percentage(best_totals, targets)
            
            return CombinationResult(
                products=best_combination,
                total_protein=best_totals['protein'],
                total_carbs=best_totals['carbs'],
                total_fat=best_totals['fat'],
                total_electrolytes=best_totals['electrolytes'],
                total_calories=best_totals['calories'],
                score=best_score,
                algorithm_used="dynamic_programming",
                target_match_percentage=target_match
            )
        
        # Sort by score and keep top candidates
        valid_combinations.sort(key=lambda x: x['score'])
        top_candidates = valid_combinations[:max_candidates]
        
        # Randomly select from top candidates
        import random
        selected = random.choice(top_candidates)
        
        target_match = self._calculate_target_match_percentage(selected['totals'], targets)
        
        return CombinationResult(
            products=selected['combination'],
            total_protein=selected['totals']['protein'],
            total_carbs=selected['totals']['carbs'],
            total_fat=selected['totals']['fat'],
            total_electrolytes=selected['totals']['electrolytes'],
            total_calories=selected['totals']['calories'],
            score=selected['score'],
            algorithm_used="dynamic_programming_random",
            target_match_percentage=target_match
        )
    
    def _simple_selection_algorithm(self, products: List[Product], targets: MacroTargets) -> CombinationResult:
        """Simple selection algorithm for large datasets."""
        # Sort products by how well they match the targets
        scored_products = []
        for product in products:
            score, totals = self.calculate_combination_score([product], targets)
            scored_products.append((product, score, totals))
        
        # Sort by score (lower is better)
        scored_products.sort(key=lambda x: x[1])
        
        # Select top products up to max_snacks
        selected_products = [p[0] for p in scored_products[:self.max_snacks]]
        
        # Calculate totals for selected products
        score, totals = self.calculate_combination_score(selected_products, targets)
        target_match = self._calculate_target_match_percentage(totals, targets)
        
        return CombinationResult(
            products=selected_products,
            total_protein=totals['protein'],
            total_carbs=totals['carbs'],
            total_fat=totals['fat'],
            total_electrolytes=totals['electrolytes'],
            total_calories=totals['calories'],
            score=score,
            algorithm_used="simple_selection",
            target_match_percentage=target_match
        )
    
    def _calculate_target_match_percentage(self, 
                                         totals: Dict[str, float], 
                                         targets: MacroTargets) -> float:
        """Calculate how well the combination matches targets (0-100%)."""
        target_values = {
            'protein': targets.target_protein_g,
            'carbs': targets.target_carbs_g,
            'fat': targets.target_fat_g,
            'electrolytes': targets.target_electrolytes_mg
        }
        
        total_diff = 0.0
        valid_targets = 0
        
        for macro, total in totals.items():
            if macro == 'calories':
                continue
                
            target = target_values[macro]
            if target > 0:
                diff = abs(total - target) / target
                total_diff += diff
                valid_targets += 1
        
        if valid_targets == 0:
            return 100.0
        
        avg_diff = total_diff / valid_targets
        match_percentage = max(0, 100 - (avg_diff * 100))
        
        return match_percentage

def optimize_macro_combination(products: List[Product], 
                             macro_targets: MacroTarget,
                             min_snacks: int = 4,
                             max_snacks: int = 10,
                             max_candidates: int = 10,
                             score_threshold: float = 1.5,
                             calorie_cap: float = None) -> CombinationResult:
    """
    Main function to optimize macro combinations using dynamic programming with randomization.
    
    Args:
        products: List of candidate products from Layer 1
        macro_targets: MacroTarget object with nutritional targets
        min_snacks: Minimum number of snacks (4-10)
        max_snacks: Maximum number of snacks (4-10)
        max_candidates: Maximum number of candidate combinations to consider
        score_threshold: Score threshold for valid combinations (lower = stricter)
        calorie_cap: If set, only consider combinations with total calories <= this value
    
    Returns:
        CombinationResult with randomly selected optimal snack combination
    """
    # Convert MacroTarget to MacroTargets
    targets = MacroTargets(
        target_protein_g=macro_targets.target_protein or 0.0,
        target_carbs_g=macro_targets.target_carbs or 0.0,
        target_fat_g=macro_targets.target_fat or 0.0,
        target_electrolytes_mg=macro_targets.target_electrolytes or 0.0
    )
    
    # Create optimizer
    optimizer = MacroOptimizer(
        min_snacks=min_snacks,
        max_snacks=max_snacks
    )
    
    # Use dynamic programming with randomization
    return optimizer.dynamic_programming_algorithm(
        products, 
        targets, 
        max_candidates=max_candidates,
        score_threshold=score_threshold,
        calorie_cap=calorie_cap
    ) 