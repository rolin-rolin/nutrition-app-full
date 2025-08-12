"""
Enhanced Embedding System for Unified User Query and Product Matching

This module provides enhanced embedding functions that create a unified vector space
for matching user queries (with soft preferences and macro targets) to product schemas.
"""

from typing import List, Dict, Any, Optional
from app.db.models import Product as ProductModel
from app.core.global_embeddings import get_embedding_model
from app.core.embedding import calculate_cosine_similarity

def generate_user_query_embedding_text(user_query: str, soft_preferences: dict = None, macro_targets: dict = None) -> str:
    """
    Generate rich text representation of user query for embedding.
    This creates a comprehensive description that can be matched against product embeddings.
    
    Args:
        user_query: Original natural language query
        soft_preferences: LLM-extracted soft preferences (flavor, texture, price, dietary)
        macro_targets: Macro targets from RAG pipeline (protein, carbs, etc.)
    
    Returns:
        String representation for embedding
    """
    parts = []
    
    # Start with the original query
    if user_query:
        parts.append(user_query)
    
    # Add soft preferences
    if soft_preferences:
        flavor_prefs = soft_preferences.get("flavor", [])
        texture_prefs = soft_preferences.get("texture", [])
        dietary_prefs = soft_preferences.get("dietary", [])
        
        if flavor_prefs:
            parts.append(f"wants {' and '.join(flavor_prefs)} flavor")
        if texture_prefs:
            parts.append(f"wants {' and '.join(texture_prefs)} texture")
        if dietary_prefs:
            parts.append(f"wants {' and '.join(dietary_prefs)}")
    
    # Add macro targets
    if macro_targets:
        if macro_targets.get("target_protein"):
            parts.append(f"needs {macro_targets['target_protein']:.0f}g protein")
        if macro_targets.get("target_carbs"):
            parts.append(f"needs {macro_targets['target_carbs']:.0f}g carbs")
        if macro_targets.get("target_calories"):
            parts.append(f"target {macro_targets['target_calories']:.0f} calories")
    
    return " ".join(parts)

def generate_user_query_embedding(user_query: str, soft_preferences: dict = None, macro_targets: dict = None) -> List[float]:
    """
    Generate embedding for user query with soft preferences and macro targets.
    
    Args:
        user_query: Original natural language query
        soft_preferences: LLM-extracted soft preferences
        macro_targets: Macro targets from RAG pipeline
    
    Returns:
        Embedding vector
    """
    model = get_embedding_model()
    embedding_text = generate_user_query_embedding_text(user_query, soft_preferences, macro_targets)
    embedding = model.encode([embedding_text])
    return embedding.tolist()[0]

def generate_enhanced_product_embedding_text(product: ProductModel) -> str:
    """
    Generate enhanced natural language text representation of a product for embedding.
    This creates a more comprehensive description that better matches user query patterns.
    """
    parts = []
    
    # Basic product info
    if product.name:
        parts.append(product.name)
    if product.brand:
        parts.append(f"{product.brand} brand")
    
    # Key matching attributes
    if product.flavor:
        parts.append(f"{product.flavor} flavor")
    if product.texture:
        parts.append(f"{product.texture} texture")
    
    # Nutrition (key for macro matching)
    if product.protein:
        parts.append(f"{product.protein}g protein")
    if product.carbs:
        parts.append(f"{product.carbs}g carbs")
    if product.calories:
        parts.append(f"{product.calories} calories")
    
    # Dietary and timing
    if product.dietary_flags:
        parts.extend(product.dietary_flags)
    if product.timing_suitability:
        parts.extend(product.timing_suitability)
    
    # Form and price
    if product.form:
        parts.append(f"{product.form} form")
    if product.price_usd:
        parts.append(f"${product.price_usd} price")
    
    # Description (if available)
    if product.description:
        parts.append(product.description)
    
    return ", ".join(parts)

def generate_enhanced_product_embedding(product: ProductModel) -> List[float]:
    """Generate enhanced embedding for product using improved text representation."""
    model = get_embedding_model()
    embedding_text = generate_enhanced_product_embedding_text(product)
    embedding = model.encode([embedding_text])
    return embedding.tolist()[0]

def calculate_similarity_score(user_embedding: List[float], product_embedding: List[float]) -> float:
    """
    Calculate similarity score between user query and product.
    Higher score = better match.
    """
    return calculate_cosine_similarity(user_embedding, product_embedding)

def rank_products_by_similarity(user_query: str, products: List[ProductModel], soft_preferences: dict = None, macro_targets: dict = None) -> List[tuple]:
    """
    Rank products by similarity to user query embedding.
    
    Args:
        user_query: User's natural language query
        products: List of products to rank
        soft_preferences: LLM-extracted soft preferences
        macro_targets: Macro targets from RAG pipeline
    
    Returns:
        List of (product, similarity_score) tuples, sorted by score descending
    """
    # Generate user query embedding
    user_embedding = generate_user_query_embedding(user_query, soft_preferences, macro_targets)
    
    # Rank products
    product_scores = []
    for product in products:
        product_embedding = generate_enhanced_product_embedding(product)
        similarity = calculate_similarity_score(user_embedding, product_embedding)
        product_scores.append((product, similarity))
    
    # Sort by similarity
    product_scores.sort(key=lambda x: x[1], reverse=True)
    return product_scores

def get_top_matching_products(user_query: str, products: List[ProductModel], top_k: int = 10, soft_preferences: dict = None, macro_targets: dict = None) -> List[ProductModel]:
    """
    Get top k products that best match the user query.
    
    Args:
        user_query: User's natural language query
        products: List of products to search
        top_k: Number of top products to return
        soft_preferences: LLM-extracted soft preferences
        macro_targets: Macro targets from RAG pipeline
    
    Returns:
        List of top matching products
    """
    ranked_products = rank_products_by_similarity(user_query, products, soft_preferences, macro_targets)
    return [product for product, score in ranked_products[:top_k]]

def debug_embedding_matching(user_query: str, product: ProductModel, soft_preferences: dict = None, macro_targets: dict = None) -> Dict[str, Any]:
    """
    Debug function to show embedding matching details.
    
    Args:
        user_query: User's natural language query
        product: Product to match against
        soft_preferences: LLM-extracted soft preferences
        macro_targets: Macro targets from RAG pipeline
    
    Returns:
        Dict with debugging information
    """
    # Generate embeddings
    user_embedding_text = generate_user_query_embedding_text(user_query, soft_preferences, macro_targets)
    user_embedding = generate_user_query_embedding(user_query, soft_preferences, macro_targets)
    
    product_embedding_text = generate_enhanced_product_embedding_text(product)
    product_embedding = generate_enhanced_product_embedding(product)
    
    # Calculate similarity
    similarity = calculate_similarity_score(user_embedding, product_embedding)
    
    return {
        "user_query": user_query,
        "user_embedding_text": user_embedding_text,
        "product_name": product.name,
        "product_embedding_text": product_embedding_text,
        "similarity_score": similarity,
        "soft_preferences": soft_preferences,
        "macro_targets": macro_targets
    }
