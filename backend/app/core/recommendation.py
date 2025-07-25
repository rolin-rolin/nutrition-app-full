import os
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
import itertools
import re
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.product import Product as ProductSchema
from app.schemas.macro_target import MacroTargetResponse
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.core.layer2_macro_optimization import optimize_macro_combination
from app.db.models import UserInput, Product, MacroTarget
from app.db.vector_store import get_product_vector_store
from sqlalchemy.orm import load_only

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

def _build_hard_filters(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Build hard filters for vector search based on user preferences."""
    hard_filters = {}
    
    # Dietary restrictions
    if preferences.get("dietary_restrictions"):
        hard_filters["dietary_flags"] = preferences["dietary_restrictions"]
    
    # Allergen exclusions
    if preferences.get("allergen_exclusions"):
        # For allergen exclusions, wellneed to filter out products that contain these allergens
        # This is handled in the vector store query
        pass
    
    # Price constraints
    if preferences.get("max_price_usd"):
        hard_filters["price_usd"] = {"$lte": preferences["max_price_usd"]}
    
    # Form preferences
    if preferences.get("form_preferences"):
        hard_filters["form"] = preferences["form_preferences"]  
    return hard_filters

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
    reasoning_steps = []

    # --- 1. Parse user query and preferences for available info ---
    has_activity_info = any([
        request.age is not None,
        request.weight_kg is not None,
        request.exercise_type is not None,
        request.exercise_duration_minutes is not None
    ])
    has_flavor_info = bool(preferences.get("flavor_preferences") or preferences.get("texture_preferences"))
    calorie_cap = None
    if preferences.get("calorie_cap"):
        try:
            calorie_cap = float(preferences["calorie_cap"])
        except (ValueError, TypeError):
            calorie_cap = None

    # --- 2. If activity info is present, generate macro targets ---
    macro_target = None
    context = ""
    if has_activity_info:
        macro_targeting_service = MacroTargetingServiceLocal()
        user_input_db = UserInput(**request.model_dump())
        context, macro_target = macro_targeting_service.get_context_and_macro_targets(user_input_db)
        reasoning_steps.append(f"Retrieved RAG context and generated macro targets: ~{macro_target.target_protein or 0:.0f}g protein, ~{macro_target.target_carbs or 0:.0f}g carbs.")
    else:
        reasoning_steps.append("No activity info detected; skipping macro targeting and optimization.")

    # --- 3. Build vector search query ---
    if has_activity_info and macro_target:
        # Use macro targets to build query
        soft_guidance = extract_soft_guidance(context)
        user_soft_prefs = []
        if preferences.get("flavor_preferences"):
            user_soft_prefs.append(f"flavor: {'/'.join(preferences['flavor_preferences'])}")
        if preferences.get("texture_preferences"):
            user_soft_prefs.append(f"texture: {'/'.join(preferences['texture_preferences'])}")
        if preferences.get("flavor_exclusions"):
            user_soft_prefs.append(f"not: {'/'.join(preferences['flavor_exclusions'])}")
        vector_query = f"{soft_guidance} {' '.join(user_soft_prefs)}"
        reasoning_steps.append(f"Built vector search query: '{vector_query}'")
    elif has_flavor_info:
        # Use only flavor/texture info
        vector_query = " ".join([
            f"flavor: {'/'.join(preferences['flavor_preferences'])}" if preferences.get("flavor_preferences") else "",
            f"texture: {'/'.join(preferences['texture_preferences'])}" if preferences.get("texture_preferences") else ""
        ]).strip()
        reasoning_steps.append(f"Built vector search query (flavor/texture only): '{vector_query}'")
    else:
        # Fallback to user_query
        vector_query = request.user_query
        reasoning_steps.append(f"Built vector search query (fallback to user_query): '{vector_query}'")

    # --- 4. Build hard filters ---
    hard_filters = _build_hard_filters(preferences)
    reasoning_steps.append(f"Built hard filters: {hard_filters}")

    # --- 5. Vector search (Layer 1) ---
    vector_store = get_product_vector_store()
    vector_results = vector_store.query_similar_products(
        query=vector_query,
        top_k=50,
        hard_filters=hard_filters if hard_filters else None,
        use_mmr=True,
        mmr_lambda=0.5
    )
    candidate_snacks = []
    for result in vector_results:
        product = (
            db.query(Product)
            .options(load_only(*(getattr(Product, c.name) for c in Product.__table__.columns)))
            .filter(Product.id == result['product_id'])
            .first()
        )
        if product:
            candidate_snacks.append(product)
    reasoning_steps.append(f"Vector search returned {len(candidate_snacks)} candidate snacks with diversity optimization.")

    # --- 6. Apply additional hard filters (ingredient exclusions) ---
    additional_filters = {
        key: preferences.get(key) for key in ["ingredient_exclusions"] if preferences.get(key)
    }
    if additional_filters:
        candidate_snacks = _apply_hard_filters(candidate_snacks, additional_filters)
        reasoning_steps.append(f"Applied additional hard filters. {len(candidate_snacks)} products remaining.")

    # --- 7. Macro optimization (Layer 2) if activity info is present ---
    if has_activity_info and macro_target:
        optimization_result = optimize_macro_combination(
            products=candidate_snacks,
            macro_targets=macro_target,
            min_snacks=4,
            max_snacks=8,
            max_candidates=10,
            score_threshold=1.5,
            calorie_cap=calorie_cap
        )
        if optimization_result:
            final_recommendations = optimization_result.products
            reasoning_steps.append(f"Layer 2 optimization selected {len(final_recommendations)} snacks with score {optimization_result.score:.3f} and {optimization_result.target_match_percentage:.1f}% target match.")
            reasoning_steps.append(f"Combination provides: {optimization_result.total_protein:.1f}g protein, {optimization_result.total_carbs:.1f}g carbs, {optimization_result.total_fat:.1f}g fat, {optimization_result.total_electrolytes:.0f}mg electrolytes, {optimization_result.total_calories:.0f} calories.")
        else:
            final_recommendations = candidate_snacks[:6]
            reasoning_steps.append(f"Layer 2 optimization failed, using top {len(final_recommendations)} candidates as fallback.")
    else:
        # No macro optimization, just return top vector search results (apply calorie cap if present)
        if calorie_cap is not None:
            filtered = []
            total_cal = 0.0
            for p in candidate_snacks:
                if (total_cal + (p.calories or 0)) <= calorie_cap:
                    filtered.append(p)
                    total_cal += (p.calories or 0)
            final_recommendations = filtered
            reasoning_steps.append(f"Applied calorie cap in filtering layer. Total calories: {total_cal:.0f}.")
        else:
            final_recommendations = candidate_snacks[:6]
            reasoning_steps.append(f"No macro optimization or calorie cap; returning top {len(final_recommendations)} vector search results.")

    # --- 8. Build API response ---
    response_products = [ProductSchema.model_validate(p, from_attributes=True) for p in final_recommendations]

    macro_target_response = None
    if macro_target:
        macro_target_created_at = macro_target.created_at or datetime.utcnow()
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
            created_at=macro_target_created_at
        )

    return RecommendationResponse(
        recommended_products=response_products,
        macro_targets=macro_target_response,
        reasoning="\n".join(reasoning_steps)
    )


