from typing import List
from app.schemas.product import Product

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