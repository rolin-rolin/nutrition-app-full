from typing import List
from app.db.models import Product as ProductModel
from sentence_transformers import SentenceTransformer
import numpy as np

# Singleton for the embedding model
_embedding_model = None

def _get_embedding_model():
    """Get or create the embedding model singleton."""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model

def generate_product_embedding_text(product: ProductModel) -> str:
    """
    Generate the natural language text representation of a product for embedding.
    This creates a pseudo-natural language string like:
    "Clif Bar, chocolate chip flavor, chewy texture, 10g protein, 40g carbs, vegan, good for post-workout recovery"
    """
    parts = []
    # Basic product info
    if product.name:
        parts.append(product.name)
    if product.brand:
        parts.append(f"{product.brand} brand")
    # Flavor and texture
    if product.flavor:
        parts.append(f"{product.flavor} flavor")
    if product.texture:
        parts.append(f"{product.texture} texture")
    # Nutrition facts
    if product.protein:
        parts.append(f"{product.protein}g protein")
    if product.carbs:
        parts.append(f"{product.carbs}g carbs")
    if product.fat:
        parts.append(f"{product.fat}g fat")
    if hasattr(product, "electrolytes_mg") and product.electrolytes_mg:
        parts.append(f"{product.electrolytes_mg}mg electrolytes")
    # Dietary and health tags
    if product.dietary_flags:
        parts.extend(product.dietary_flags)
    if product.tags:
        parts.extend(product.tags)
    if product.timing_suitability:
        parts.extend(product.timing_suitability)
    # Form
    if product.form:
        parts.append(f"{product.form} form")
    # Description (if available)
    if product.description:
        parts.append(product.description)
    return ", ".join(parts)

def generate_product_embedding(product: ProductModel) -> List[float]:
    """Use sentence-transformers to convert product data to a vector."""
    model = _get_embedding_model()
    embedding_text = generate_product_embedding_text(product)
    embedding = model.encode([embedding_text])
    return embedding.tolist()[0]

def generate_query_embedding(query: str) -> List[float]:
    """Use the same embedding model for user queries."""
    model = _get_embedding_model()
    embedding = model.encode([query])
    return embedding.tolist()[0]

def calculate_cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Calculate cosine similarity between two embeddings."""
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    # Normalize vectors
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    # Calculate cosine similarity
    similarity = np.dot(vec1, vec2) / (norm1 * norm2)
    return float(similarity) 