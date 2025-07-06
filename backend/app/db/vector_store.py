from typing import List

"""
Responsible for storing and retrieving embeddings from a vector database

"""

def add_product_embedding(product_id: int, embedding: List[float]):
    """
    Store embedding in vector DB.
    """
    pass

def query_similar_products(query_embedding: List[float], top_k: int = 10) -> List[int]:
    """
    Return product IDs of most similar products.
    """
    pass 