from app.core.enhanced_embedding import get_top_matching_products, rank_products_by_similarity
import os
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
import itertools
import re
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse, EnhancedRecommendationResponse, UserProfileInfo, BundleStats, PreferenceInfo, KeyPrinciple
from app.schemas.product import Product as ProductSchema
from app.schemas.macro_target import MacroTargetResponse
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.core.layer2_macro_optimization import optimize_macro_combination
from app.db.models import UserInput, Product, MacroTarget
from app.db.vector_store import get_product_vector_store
from sqlalchemy.orm import load_only

# Module-level singleton for MacroTargetingServiceLocal
_macro_service_instance = None

def get_macro_service():
    """Get singleton instance of MacroTargetingServiceLocal to avoid multiple expensive initializations."""
    global _macro_service_instance
    if _macro_service_instance is None:
        _macro_service_instance = MacroTargetingServiceLocal()
    return _macro_service_instance

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

def _build_hard_filters_from_llm_extraction(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build hard filters from LLM-extracted preferences for pre-filtering products.
    
    Args:
        preferences: Dictionary containing LLM-extracted preferences with hard_filters
        
    Returns:
        Dictionary of hard filters for product filtering
    """
    hard_filters = {}
    
    # Get hard filters from LLM extraction
    hard_filters_data = preferences.get("hard_filters", {})
    
    # Dietary restrictions - check against dietary_flags, diet fields
    dietary_requirements = hard_filters_data.get("dietary", [])
    if dietary_requirements:
        hard_filters["dietary_requirements"] = dietary_requirements
    
    # Allergen restrictions - check against allergens field
    allergen_restrictions = hard_filters_data.get("allergens", [])
    if allergen_restrictions:
        hard_filters["allergen_restrictions"] = allergen_restrictions
    
    # Note: Price is NOT a hard filter - it's a soft preference for optimization
    # Price constraints should be handled during macro optimization or final selection
    
    return hard_filters

def _pre_filter_products_by_hard_constraints(db: Session, hard_filters: Dict[str, Any]) -> List[Product]:
    """
    Pre-filter products based on hard constraints before vector search.
    
    Args:
        db: Database session
        hard_filters: Dictionary of hard filters from LLM extraction
        
    Returns:
        List of products that meet all hard constraints
    """
    # Start with all products
    query = db.query(Product)
    
    # Apply dietary restrictions
    dietary_requirements = hard_filters.get("dietary_requirements", [])
    if dietary_requirements:
        # Products must have ALL required dietary flags
        for requirement in dietary_requirements:
            # Check both dietary_flags and diet fields
            query = query.filter(
                (Product.dietary_flags.contains([requirement])) |
                (Product.diet == requirement) |
                (Product.diet.contains([requirement]))
            )
    
    # Apply allergen restrictions - exclude products that contain restricted allergens
    allergen_restrictions = hard_filters.get("allergen_restrictions", [])
    if allergen_restrictions:
        # Use a more reliable approach for SQLite JSON filtering
        for allergen in allergen_restrictions:
            # Exclude products that contain this allergen
            # Use JSON_ARRAY_CONTAINS for SQLite or fallback to Python filtering
            query = query.filter(
                ~(Product.allergens.contains([allergen]))
            )
        
        # Execute query and do additional Python-level filtering as backup
        filtered_products = query.all()
        
        # Additional Python-level filtering to ensure allergens are properly excluded
        final_filtered = []
        for product in filtered_products:
            product_allergens = product.allergens or []
            # Check if any restricted allergen is in this product's allergens
            has_restricted_allergen = any(allergen in product_allergens for allergen in allergen_restrictions)
            if not has_restricted_allergen:
                final_filtered.append(product)
        
        return final_filtered
    
    # Note: Price is NOT applied here - it's a soft constraint for optimization
    
    # Execute query and return results
    filtered_products = query.all()
    
    return filtered_products

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
    
    # Initialize service once at the beginning
    macro_targeting_service = get_macro_service()
    
    # Extract preferences from user query if not provided
    if not preferences and request.user_query:
        try:
            # Use existing service for preference extraction
            extracted_fields = macro_targeting_service.extract_fields_from_query(request.user_query)
            
            # Convert LLM extracted fields to preferences format
            if extracted_fields:
                # Extract LLM fields
                soft_prefs = extracted_fields.get("soft_preferences", {})
                hard_filters_data = extracted_fields.get("hard_filters", {})
                
                # Set preferences in the expected format
                preferences = {
                    "soft_preferences": {
                        "flavor": soft_prefs.get("flavor", []),
                        "texture": soft_prefs.get("texture", []),
                        "dietary": []  # Will be populated by macro targeting service
                    },
                    "flavor_preferences": soft_prefs.get("flavor", []),  # Legacy format support
                    "texture_preferences": soft_prefs.get("texture", []),  # Legacy format support
                    "hard_filters": {
                        "dietary": hard_filters_data.get("dietary", []),
                        "allergens": hard_filters_data.get("allergens", [])
                    },
                    "calorie_cap": extracted_fields.get("calorie_cap")
                }
                
                # Build summary for reasoning
                soft_preferences_list = []
                soft_preferences_list.extend(soft_prefs.get("flavor", []))
                soft_preferences_list.extend(soft_prefs.get("texture", []))
                
                hard_filters_list = []
                hard_filters_list.extend(hard_filters_data.get("dietary", []))
                hard_filters_list.extend(hard_filters_data.get("allergens", []))
                
                reasoning_steps.append(f"Extracted preferences from query: soft={soft_preferences_list}, hard={hard_filters_list}")
        except Exception as e:
            reasoning_steps.append(f"Failed to extract preferences from query: {str(e)}")
            preferences = {}

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

    # --- 2. Always generate macro targets (with defaults if needed) ---
    macro_target = None
    context = ""
    user_input_db = None
    
    # Use existing macro targeting service (already initialized)
    
    if has_activity_info:
        # Use structured fields from request
        user_input_db = UserInput(**request.model_dump())
        context, macro_target = macro_targeting_service.get_context_and_macro_targets(user_input_db)
        reasoning_steps.append(f"Retrieved RAG context and generated macro targets: ~{macro_target.target_protein or 0:.0f}g protein, ~{macro_target.target_carbs or 0:.0f}g carbs.")
    else:
        # Try to extract activity info from natural language query
        try:
            user_input_db, macro_target = macro_targeting_service.generate_macro_targets_from_query(request.user_query, db)
            context = macro_targeting_service.retrieve_context_by_metadata(user_input_db)
            reasoning_steps.append(f"Extracted activity info from query and generated macro targets: ~{macro_target.target_protein or 0:.0f}g protein, ~{macro_target.target_carbs or 0:.0f}g carbs.")
        except Exception as e:
            # If extraction fails, create a default user input and generate macro targets
            reasoning_steps.append(f"Failed to extract activity info from query, using default values. Error: {str(e)}")
            
            # Create default user input with default values
            default_user_input = UserInput(
                user_query=request.user_query,
                age=21,  # Default age
                weight_kg=70.0,  # Default weight
                exercise_type="cardio",  # Default exercise type
                exercise_duration_minutes=60  # Default duration
            )
            user_input_db = default_user_input
            context, macro_target = macro_targeting_service.get_context_and_macro_targets(default_user_input)
            reasoning_steps.append(f"Generated macro targets with default values: ~{macro_target.target_protein or 0:.0f}g protein, ~{macro_target.target_carbs or 0:.0f}g carbs.")

    # --- 3. Pre-filter products by hard constraints from LLM extraction ---
    hard_filters = _build_hard_filters_from_llm_extraction(preferences)
    if hard_filters:
        pre_filtered_products = _pre_filter_products_by_hard_constraints(db, hard_filters)
        reasoning_steps.append(f"Pre-filtered products by hard constraints: {len(pre_filtered_products)} products remaining from {db.query(Product).count()} total.")
        
        # Log what filters were applied
        filter_details = []
        if hard_filters.get("dietary_requirements"):
            filter_details.append(f"dietary: {hard_filters['dietary_requirements']}")
        if hard_filters.get("allergen_restrictions"):
            filter_details.append(f"allergens: {hard_filters['allergen_restrictions']}")
        if filter_details:
            reasoning_steps.append(f"Applied hard filters: {', '.join(filter_details)}")
    else:
        pre_filtered_products = db.query(Product).all()
        reasoning_steps.append("No hard constraints found; using all products for vector search.")

    # --- 4. Build vector search query ---
    if macro_target:
        # Use macro targets to build query (always available now)
        soft_guidance = extract_soft_guidance(context)
        user_soft_prefs = []
        if preferences.get("flavor_preferences"):
            user_soft_prefs.append(f"flavor: {'/'.join(preferences['flavor_preferences'])}")
        if preferences.get("texture_preferences"):
            user_soft_prefs.append(f"texture: {'/'.join(preferences['texture_preferences'])}")
        if preferences.get("flavor_exclusions"):
            user_soft_prefs.append(f"not: {'/'.join(preferences['flavor_exclusions'])}")
        
        # Add high-protein preference if detected from strength activities
        if preferences.get("soft_preferences", {}).get("dietary"):
            dietary_prefs = preferences["soft_preferences"]["dietary"]
            if "high-protein" in dietary_prefs:
                user_soft_prefs.append("high-protein")
                reasoning_steps.append("Added high-protein preference based on strength activity detection")
        
        vector_query = f"{soft_guidance} {' '.join(user_soft_prefs)}"
        reasoning_steps.append(f"Built vector search query with macro guidance: '{vector_query}'")
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

    # --- 5. Vector search on pre-filtered products (Layer 1) ---
    vector_store = get_product_vector_store()
    
    # Check if we have soft preferences (including high-protein from strength activities)
    has_soft_preferences = bool(
        preferences.get("flavor_preferences") or 
        preferences.get("texture_preferences") or
        preferences.get("soft_preferences", {}).get("dietary")
    )
    
    # If we have soft preferences, use enhanced embedding system
    if has_soft_preferences and macro_target:
        # Use enhanced embedding system for better matching with soft preferences
        from app.core.enhanced_embedding import _enhanced_vector_search_with_embeddings
        
        # Prepare soft preferences for enhanced embedding
        soft_preferences = {}
        if preferences.get("flavor_preferences"):
            soft_preferences["flavor"] = preferences["flavor_preferences"]
        if preferences.get("texture_preferences"):
            soft_preferences["texture"] = preferences["texture_preferences"]
        if preferences.get("soft_preferences", {}).get("dietary"):
            soft_preferences["dietary"] = preferences["soft_preferences"]["dietary"]
        
        # Prepare macro targets for enhanced embedding
        macro_targets = {
            "target_protein": macro_target.target_protein,
            "target_carbs": macro_target.target_carbs,
            "target_calories": macro_target.target_calories
        }
        
        # Use enhanced embedding system
        candidate_snacks = _enhanced_vector_search_with_embeddings(
            user_query=vector_query,
            pre_filtered_products=pre_filtered_products,
            soft_preferences=soft_preferences,
            macro_targets=macro_targets
        )
        reasoning_steps.append(f"Enhanced embedding search returned {len(candidate_snacks)} candidate snacks with soft preferences.")
    else:
        # Use standard vector search
        # If we have pre-filtered products, we need to do vector search on that subset
        if len(pre_filtered_products) < db.query(Product).count():
            # We have hard filters applied, so we need to do vector search only on pre-filtered products
            # Since the vector store contains all products, we'll do the search and then filter results
            
            # Do vector search on all products first, then filter to our pre-filtered subset
            vector_results = vector_store.query_similar_products(
                query=vector_query,
                top_k=100,  # Get more candidates since we'll filter
                hard_filters=None,  # Don't use vector store hard filters since we pre-filtered
                use_mmr=True,
                mmr_lambda=0.5
            )
            
            # Filter results to only include pre-filtered products
            pre_filtered_ids = set(p.id for p in pre_filtered_products)
            filtered_vector_results = []
            seen_product_ids = set()  # Track seen product IDs to avoid duplicates
            
            for result in vector_results:
                product_id = result['product_id']
                if product_id in pre_filtered_ids and product_id not in seen_product_ids:
                    filtered_vector_results.append(result)
                    seen_product_ids.add(product_id)
            
            # Take top results from filtered subset
            vector_results = filtered_vector_results[:50]
            reasoning_steps.append(f"Vector search on pre-filtered products returned {len(vector_results)} candidates.")
        else:
            # No hard filters, do normal vector search on all products
            vector_results = vector_store.query_similar_products(
                query=vector_query,
                top_k=50,
                hard_filters=None,  # We already pre-filtered
                use_mmr=True,
                mmr_lambda=0.5
            )
            reasoning_steps.append(f"Vector search returned {len(vector_results)} candidate snacks with diversity optimization.")

    # --- 6. Convert vector results to Product objects ---
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
    
    reasoning_steps.append(f"Vector search returned {len(candidate_snacks)} candidate snacks.")

    # --- 7. Apply additional hard filters (ingredient exclusions) ---
    additional_filters = {
        key: preferences.get(key) for key in ["ingredient_exclusions"] if preferences.get(key)
    }
    if additional_filters:
        candidate_snacks = _apply_hard_filters(candidate_snacks, additional_filters)
        reasoning_steps.append(f"Applied additional hard filters. {len(candidate_snacks)} products remaining.")

    # --- 8. Macro optimization (Layer 2) if macro targets are available ---
    optimization_result = None
    if macro_target:
        optimization_result = optimize_macro_combination(
            products=candidate_snacks,
            macro_targets=macro_target,
            min_snacks=1,
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

    # --- 9. Build Enhanced API response ---
    response_products = [ProductSchema.model_validate(p, from_attributes=True) for p in final_recommendations]

    # Build user profile info for display (always create)
    user_profile = None
    # Use extracted user_input_db if available, otherwise use request fields
    source_data = user_input_db if user_input_db else request
    
    age_display = f"{source_data.age} years old" if source_data.age else "using default age 21"
    weight_display = f"{source_data.weight_kg}kg" if source_data.weight_kg else "using default 70kg weight"
    
    if source_data.exercise_type and source_data.exercise_duration_minutes:
        exercise_display = f"{source_data.exercise_type} for {source_data.exercise_duration_minutes} minutes"
    elif source_data.exercise_type:
        exercise_display = f"{source_data.exercise_type} (using default 60-minute duration)"
    elif source_data.exercise_duration_minutes:
        exercise_display = f"cardio for {source_data.exercise_duration_minutes} minutes (using default exercise type)"
    else:
        exercise_display = "cardio (using default 60-minute duration)"
    
    user_profile = UserProfileInfo(
        age=source_data.age,
        weight_kg=source_data.weight_kg,
        exercise_type=source_data.exercise_type,
        exercise_duration_minutes=source_data.exercise_duration_minutes,
        age_display=age_display,
        weight_display=weight_display,
        exercise_display=exercise_display
    )

    # Build bundle stats (always calculate)
    bundle_stats = None
    if optimization_result:
        bundle_stats = BundleStats(
            total_protein=optimization_result.total_protein,
            total_carbs=optimization_result.total_carbs,
            total_fat=optimization_result.total_fat,
            total_electrolytes=optimization_result.total_electrolytes,
            total_calories=optimization_result.total_calories,
            num_snacks=len(final_recommendations),
            target_match_percentage=optimization_result.target_match_percentage
        )
    else:
        # Calculate totals manually if no optimization result
        total_protein = sum(p.protein or 0 for p in final_recommendations)
        total_carbs = sum(p.carbs or 0 for p in final_recommendations)
        total_fat = sum(p.fat or 0 for p in final_recommendations)
        total_electrolytes = sum(p.electrolytes_mg or 0 for p in final_recommendations)
        total_calories = sum(p.calories or 0 for p in final_recommendations)
        
        bundle_stats = BundleStats(
            total_protein=total_protein,
            total_carbs=total_carbs,
            total_fat=total_fat,
            total_electrolytes=total_electrolytes,
            total_calories=total_calories,
            num_snacks=len(final_recommendations),
            target_match_percentage=0.0  # No optimization, so no target match
        )

    # Build preferences info
    soft_prefs = []
    hard_filters = []
    
    # Extract soft preferences
    if preferences.get("flavor_preferences"):
        soft_prefs.extend([f"{pref} flavor" for pref in preferences["flavor_preferences"]])
    if preferences.get("texture_preferences"):
        soft_prefs.extend([f"{pref} texture" for pref in preferences["texture_preferences"]])
    if preferences.get("soft_preferences", {}).get("dietary"):
        soft_prefs.extend(preferences["soft_preferences"]["dietary"])
    
    # Extract hard filters
    if preferences.get("dietary_requirements"):
        hard_filters.extend(preferences["dietary_requirements"])
    if preferences.get("allergen_restrictions"):
        hard_filters.extend([f"no {allergen}" for allergen in preferences["allergen_restrictions"]])
    if preferences.get("ingredient_exclusions"):
        hard_filters.extend([f"no {ingredient}" for ingredient in preferences["ingredient_exclusions"]])
    
    preferences_info = PreferenceInfo(
        soft_preferences=soft_prefs,
        hard_filters=hard_filters
    )

    # Extract key principles from knowledge document
    key_principles = []
    if macro_target and macro_target.rag_context:
        # Use existing service instance
        principles = macro_targeting_service.extract_key_principles(macro_target.rag_context, num_principles=2)
        key_principles = [KeyPrinciple(principle=principle) for principle in principles]

    # Build macro target response
    macro_target_response = None
    timing_breakdown = None
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
        
        # Create timing breakdown for frontend display
        from app.schemas.recommendation import TimingMacroBreakdown
        timing_breakdown = TimingMacroBreakdown(
            pre_workout=macro_target.pre_workout_macros,
            during_workout=macro_target.during_workout_macros,
            post_workout=macro_target.post_workout_macros
        )

    return EnhancedRecommendationResponse(
        recommended_products=response_products,
        macro_targets=macro_target_response,
        timing_breakdown=timing_breakdown,
        reasoning="\n".join(reasoning_steps),
        user_profile=user_profile,
        bundle_stats=bundle_stats,
        preferences=preferences_info,
        key_principles=key_principles
    )


def _enhanced_vector_search_with_embeddings(user_query: str, pre_filtered_products: List[Product], soft_preferences: dict = None, macro_targets: dict = None) -> List[Product]:
    """Enhanced vector search using unified embeddings for user queries and products."""
    # Use the enhanced embedding system to rank products
    ranked_products = rank_products_by_similarity(
        user_query, 
        pre_filtered_products, 
        soft_preferences, 
        macro_targets
    )
    # Return top products (limit to reasonable number for optimization)
    return [product for product, score in ranked_products[:50]]
