from typing import List
from app.schemas.product import Product

"""
Low-level embedding functions for 

Uses openai's api to generate embeddings for products and user queries.

- Functions to generate embeddings for products (using OpenAI, HuggingFace, etc.)
- Functions to generate embeddings for user queries
- Interface to store/retrieve embeddings (will call to vector_store.py)
"""

def generate_product_embedding(product: Product) -> List[float]:
    """
    Use an embedding model to convert product data to a vector.
    """
    pass

def generate_query_embedding(query: str) -> List[float]:
    """
    Use the same embedding model for user queries.
    """
    pass 