import os
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
import itertools
import re
from dotenv import load_dotenv
load_dotenv()
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.product import Product as ProductSchema
from app.schemas.macro_target import MacroTargetResponse
from app.core.macro_targeting import MacroTargetingService
from app.db.models import UserInput, Product, MacroTarget

def _build_augmented_query(macro_target: MacroTarget, preferences: Dict[str, Any]) -> str:
    """Builds a natural language query for vector search using soft preferences."""
    query_parts = [f"A snack with around {macro_target.target_protein or 0:.0f}g of protein and {macro_target.target_carbs or 0:.0f}g of carbs."]

    if preferences.get("texture_preferences"):
        query_parts.append(f"It should have a {' or '.join(preferences['texture_preferences'])} texture.")
    if preferences.get("flavor_preferences"):
        query_parts.append(f"It should taste {' or '.join(preferences['flavor_preferences'])}.")
    if preferences.get("flavor_exclusions"):
        query_parts.append(f"It should not be {' or '.join(preferences['flavor_exclusions'])}.")
        
    return " ".join(query_parts)

def _apply_hard_filters(products: List[Product], preferences: Dict[str, Any]) -> List[Product]:
    """Filters a list of products based on hard constraints."""
    filtered_products = []
    
    dietary_restrictions = preferences.get("dietary_restrictions", [])
    ingredient_exclusions = preferences.get("ingredient_exclusions", [])
    
    if not dietary_restrictions and not ingredient_exclusions:
        return products

    for product in products:
        product_flags = product.dietary_flags or []
        if dietary_restrictions and not all(flag in product_flags for flag in dietary_restrictions):
            continue

        product_description = (product.description or "").lower()
        if ingredient_exclusions and any(excl.lower() in product_description for excl in ingredient_exclusions):
            continue
            
        filtered_products.append(product)
        
    return filtered_products

def _calculate_combination_score(combination: List[Product], macro_targets: MacroTarget) -> float:
    """Calculate how well a combination of snacks matches the macro targets."""
    total_protein = sum(p.protein or 0 for p in combination)
    total_carbs = sum(p.carbs or 0 for p in combination)
    total_fat = sum(p.fat or 0 for p in combination)
    total_calories = sum(p.calories or 0 for p in combination)
    
    # Calculate percentage differences from targets
    protein_diff = abs(total_protein - (macro_targets.target_protein or 0)) / max(macro_targets.target_protein or 1, 1)
    carbs_diff = abs(total_carbs - (macro_targets.target_carbs or 0)) / max(macro_targets.target_carbs or 1, 1)
    fat_diff = abs(total_fat - (macro_targets.target_fat or 0)) / max(macro_targets.target_fat or 1, 1)
    calories_diff = abs(total_calories - (macro_targets.target_calories or 0)) / max(macro_targets.target_calories or 1, 1)
    
    # Lower score is better (closer to targets)
    total_score = protein_diff + carbs_diff + fat_diff + calories_diff
    
    # Penalize combinations that are too far from targets
    if total_score > 2.0:  # More than 200% off target
        total_score *= 2
    
    return total_score

def _find_optimal_snack_combination(products: List[Product], macro_targets: MacroTarget, 
                                   min_snacks: int = 5, max_snacks: int = 10) -> List[Product]:
    """Find the best combination of 5-10 snacks that collectively meet macro targets."""
    if len(products) < min_snacks:
        return products[:min_snacks] if len(products) >= min_snacks else products
    
    best_combination = None
    best_score = float('inf')
    
    # Try combinations of different sizes
    for combo_size in range(min_snacks, min(max_snacks + 1, len(products) + 1)):
        # Use itertools to generate combinations efficiently
        for combination in itertools.combinations(products, combo_size):
            score = _calculate_combination_score(list(combination), macro_targets)
            
            if score < best_score:
                best_score = score
                best_combination = list(combination)
    
    return best_combination or products[:min_snacks]

def extract_soft_guidance(context: str) -> str:
    """Extract soft guidance lines from the RAG context."""
    # Simple heuristic: lines that start with advice verbs
    advice_verbs = [
        r"prioritize", r"favor", r"choose", r"avoid", r"prefer", r"focus on", r"look for", r"select"
    ]
    pattern = re.compile(rf"^({'|'.join(advice_verbs)})", re.IGNORECASE)
    lines = context.splitlines()
    guidance_lines = [line.strip() for line in lines if pattern.match(line.strip())]
    # Fallback: if nothing found, use the first 2 lines
    if not guidance_lines:
        guidance_lines = lines[:2]
    return " ".join(guidance_lines)

async def get_recommendations(request: RecommendationRequest, db: Session) -> RecommendationResponse:
    preferences = request.preferences or {}
    
    # 1. Get RAG Context and Macro Targets (Unified)
    macro_targeting_service = MacroTargetingService(openai_api_key=os.getenv("OPENAI_API_KEY"))
    user_input_db = UserInput(**request.model_dump())
    context, macro_target = macro_targeting_service.get_context_and_macro_targets(user_input_db)
    
    reasoning_steps = [f"Retrieved RAG context and generated macro targets: ~{macro_target.target_protein or 0:.0f}g protein, ~{macro_target.target_carbs or 0:.0f}g carbs."]
    
    # 2. Extract Soft Guidance from Context
    soft_guidance = extract_soft_guidance(context)
    reasoning_steps.append(f"Extracted soft guidance from context: '{soft_guidance}'")
    
    # 3. Build Vector Search Query (Soft Guidance + User Soft Preferences)
    user_soft_prefs = []
    if preferences.get("flavor_preferences"):
        user_soft_prefs.append(f"flavor: {'/'.join(preferences['flavor_preferences'])}")
    if preferences.get("texture_preferences"):
        user_soft_prefs.append(f"texture: {'/'.join(preferences['texture_preferences'])}")
    if preferences.get("flavor_exclusions"):
        user_soft_prefs.append(f"not: {'/'.join(preferences['flavor_exclusions'])}")
    vector_query = f"{soft_guidance} {' '.join(user_soft_prefs)}"
    reasoning_steps.append(f"Built vector search query: '{vector_query}'")
    
    # 4. Retrieve Snacks Using Vector Query (Simulated)
    # TODO: Replace with real vector search
    all_products = db.query(Product).all()
    candidate_snacks = all_products  # Simulate: use all products for now
    reasoning_steps.append(f"Simulated vector search. {len(candidate_snacks)} candidate snacks.")
    
    # 5. Apply Hard Filters
    hard_constraints = {
        key: preferences.get(key) for key in 
        ["dietary_restrictions", "ingredient_exclusions"] if preferences.get(key)
    }
    filtered_products = _apply_hard_filters(candidate_snacks, hard_constraints)
    reasoning_steps.append(f"Applied hard filters for {list(hard_constraints.keys())}. {len(filtered_products)} products remaining.")

    # 6. Find Optimal Combination (5-10 snacks)
    final_recommendations = _find_optimal_snack_combination(filtered_products, macro_target, min_snacks=5, max_snacks=10)
    
    # Calculate actual totals from the combination
    total_protein = sum(p.protein or 0 for p in final_recommendations)
    total_carbs = sum(p.carbs or 0 for p in final_recommendations)
    total_fat = sum(p.fat or 0 for p in final_recommendations)
    total_calories = sum(p.calories or 0 for p in final_recommendations)
    
    reasoning_steps.append(f"Found optimal combination of {len(final_recommendations)} snacks that provides: {total_protein:.1f}g protein, {total_carbs:.1f}g carbs, {total_fat:.1f}g fat, {total_calories:.0f} calories.")

    response_products = [ProductSchema.model_validate(p, from_attributes=True) for p in final_recommendations]

    
    # Convert MacroTarget to MacroTargetResponse for the API response
    macro_target_response = MacroTargetResponse(
        target_calories=macro_target.target_calories,
        target_protein=macro_target.target_protein,
        target_carbs=macro_target.target_carbs,
        target_fat=macro_target.target_fat,
        target_electrolytes=macro_target.target_electrolytes,
        pre_workout_macros=macro_target.pre_workout_macros,
        during_workout_macros=macro_target.during_workout_macros,
        post_workout_macros=macro_target.post_workout_macros,
        reasoning=macro_target.reasoning,
        rag_context=macro_target.rag_context,
        confidence_score=macro_target.confidence_score,
        created_at=macro_target.created_at
    )
    
    return RecommendationResponse(
        recommended_products=response_products,
        macro_targets=macro_target_response,
        reasoning="\n".join(reasoning_steps)
    )


