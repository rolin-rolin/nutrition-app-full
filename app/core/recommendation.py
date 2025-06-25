import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.product import Product as ProductSchema
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

async def get_recommendations(request: RecommendationRequest, db: Session) -> RecommendationResponse:
    preferences = request.preferences or {}
    
    # 1. Get Macro Targets
    macro_targeting_service = MacroTargetingService(openai_api_key=os.getenv("OPENAI_API_KEY"))
    user_input_db = UserInput(**request.dict())
    macro_target = macro_targeting_service.generate_macro_targets(user_input_db)
    
    reasoning_steps = [f"Generated macro targets: ~{macro_target.target_protein or 0:.0f}g protein, ~{macro_target.target_carbs or 0:.0f}g carbs."]
    
    # 2. Augment Query (Soft Preferences)
    soft_preferences = {
        key: preferences.get(key) for key in 
        ["flavor_preferences", "texture_preferences", "flavor_exclusions"] if preferences.get(key)
    }
    augmented_query = _build_augmented_query(macro_target, soft_preferences)
    reasoning_steps.append(f"Augmented search query with soft preferences: '{augmented_query}'")
    
    # 3. Vector Search (Simulated)
    all_products = db.query(Product).all()
    reasoning_steps.append(f"Simulating vector search with augmented query. Starting with {len(all_products)} total products.")
    
    # 4. Apply Hard Filters
    hard_constraints = {
        key: preferences.get(key) for key in 
        ["dietary_restrictions", "ingredient_exclusions"] if preferences.get(key)
    }
    filtered_products = _apply_hard_filters(all_products, hard_constraints)
    reasoning_steps.append(f"Applied hard filters for {list(hard_constraints.keys())}. {len(filtered_products)} products remaining.")

    # 5. Rank and Select Final Products (Simplified)
    final_recommendations = filtered_products[:5]
    reasoning_steps.append(f"Selected the top {len(final_recommendations)} products. (Ranking logic to be implemented).")

    response_products = [ProductSchema.from_orm(p) for p in final_recommendations]
    
    return RecommendationResponse(
        recommended_products=response_products,
        reasoning="\n".join(reasoning_steps)
    )


