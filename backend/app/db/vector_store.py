from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings
import numpy as np
from sentence_transformers import SentenceTransformer

from app.db.models import Product
from app.core.embedding import generate_product_embedding_text, generate_query_embedding

"""
Responsible for storing and retrieving embeddings from a vector database

Uses Chroma for vector storage and similarity search with hard filtering and MMR diversity.
"""

class ProductVectorStore:
    def __init__(self, persist_directory: str = "./data/product_vector_store"):
        """
        Initialize the product vector store.

        Args:
            persist_directory: Path to store Chroma vector database
        """
        self.persist_directory = persist_directory
        # Lazy load embeddings only when needed
        self._embeddings = None
        self._initialize_vectorstore()
    
    @property
    def embeddings(self):
        """Lazy load embeddings only when needed."""
        if self._embeddings is None:
            self._embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        return self._embeddings

    def _get_embedding_function(self):
        """
        Create a LangChain-compatible embedding function from sentence-transformers.
        """
        class SentenceTransformerEmbeddings(Embeddings):
            def __init__(self, model):
                self.model = model

            def embed_documents(self, texts):
                embeddings = self.model.encode(texts)
                return embeddings.tolist()

            def embed_query(self, text):
                embedding = self.model.encode([text])
                return embedding.tolist()[0]

        return SentenceTransformerEmbeddings(self.embeddings)

    def _initialize_vectorstore(self):
        """
        Initialize the vector store.
        """
        try:
            # Try to load existing vector store
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self._get_embedding_function()
            )
            print(f"Loaded existing product vector store from {self.persist_directory}")
        except Exception as e:
            print(f"Failed to load existing vector store: {e}")
            print("Creating new product vector store...")
            self._create_vectorstore()

    def _create_vectorstore(self):
        """
        Create a new vector store.
        """
        # Create empty vector store
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self._get_embedding_function()
        )
        print(f"Created new product vector store at {self.persist_directory}")

    def add_product_embedding(self, product: Product):
        """
        Store product embedding in vector DB.

        Args:
            product: Product object with all metadata
        """
        # Generate embedding text
        embedding_text = generate_product_embedding_text(product)

        # Generate embedding
        embedding = self.embeddings.encode([embedding_text])

        # Create metadata for filtering (convert lists to strings for Chroma compatibility)
        metadata = {
            'product_id': product.id,
            'name': product.name,
            'brand': product.brand,
            'flavor': product.flavor,
            'texture': product.texture,
            'form': product.form,
            'price_usd': product.price_usd,
            'dietary_flags': ', '.join(product.dietary_flags or []),
            'tags': ', '.join(product.tags or []),
            'allergens': ', '.join(product.allergens or []),
            'timing_suitability': ', '.join(product.timing_suitability or [])
        }

        # Add to vector store
        from langchain.schema import Document
        doc = Document(
            page_content=embedding_text,
            metadata=metadata
        )
        self.vectorstore.add_documents([doc])

        # Update product with embedding info
        product.embedding = embedding.tolist()[0]
        product.embedding_text = embedding_text

    def query_similar_products(
        self,
        query: str,
        top_k: int = 20,
        hard_filters: Optional[Dict[str, Any]] = None,
        use_mmr: bool = True,
        mmr_lambda: float = 0.8  # Higher lambda = more emphasis on relevance
    ) -> List[Dict[str, Any]]:
        """
        Return similar products with hard filtering and optional MMR diversity.

        Args:
            query: Natural language query
            top_k: Number of results to retrieve
            hard_filters: Dict of hard constraints (e.g., {"dietary_flags": ["vegan"]})
            use_mmr: Whether to apply Maximal Marginal Relevance for diversity
            mmr_lambda: MMR parameter (0.0 = max diversity, 10 = max relevance)

        Returns:
            List of product results with scores
        """
        # Retrieve candidates using similarity search first
        results = self.vectorstore.similarity_search_with_score(
            query,
            k=top_k * 3  # Get more candidates for filtering and MMR
        )
        
        # Convert to candidates with similarity scores
        candidates = []
        for doc, score in results:
            candidates.append({
                'product_id': doc.metadata['product_id'],
                'metadata': doc.metadata,
                'score': score,
                'text': doc.page_content
            })
        
        # Apply hard filters in Python if specified
        if hard_filters:
            filtered_candidates = []
            for candidate in candidates:
                matches_all_filters = True
                for key, value in hard_filters.items():
                    if key == "dietary_flags" and isinstance(value, list):
                        # Check if any dietary flag is in the comma-separated string
                        stored_flags = candidate['metadata'].get(key, "").split(", ")
                        if not any(flag in stored_flags for flag in value):
                            matches_all_filters = False
                            break
                    elif isinstance(value, list):
                        # For other list fields, check exact match
                        stored_value = candidate['metadata'].get(key, "")
                        if stored_value not in value:
                            matches_all_filters = False
                            break
                    else:
                        # For single values, check exact match
                        if candidate['metadata'].get(key) != value:
                            matches_all_filters = False
                            break
                
                if matches_all_filters:
                    filtered_candidates.append(candidate)
            
            candidates = filtered_candidates

        # Apply MMR if requested (very conservative approach)
        if use_mmr and len(candidates) > 1:
            # Only apply MMR to the top 3 results and only if there's significant diversity benefit
            top_candidates = candidates[:3]
            remaining_candidates = candidates[3:]
            
            # Apply MMR to top candidates
            top_candidates = self._apply_mmr(top_candidates, query, mmr_lambda)
            
            # Combine MMR results with remaining candidates
            candidates = top_candidates + remaining_candidates

        # Return top_k results
        return candidates[:top_k]

    def _apply_mmr(self, candidates: List[Dict], query: str, lambda_param: float) -> List[Dict]:
        """
        Apply Maximal Marginal Relevance for diversity.

        Args:
            candidates: List of candidate products with scores
            query: Original query
            lambda_param: MMR parameter (0.0 = max diversity, 10 = max relevance)

        Returns:
            Reordered candidates with diversity
        """
        if len(candidates) <= 1:
            return candidates

        # Sort by relevance score
        candidates.sort(key=lambda x: x['score'], reverse=True)

        # Initialize selected and remaining
        selected = [candidates[0]]
        remaining = candidates[1:]

        # Apply MMR selection (very conservative)
        while remaining and len(selected) < len(candidates):
            # Calculate MMR scores
            mmr_scores = []
            for candidate in remaining:
                # Relevance score (already calculated)
                relevance = candidate['score']

                # Diversity score (very conservative)
                diversity = 0.0
                if selected:
                    similarities = []
                    for selected_item in selected:
                        # Only consider diversity if forms are very different
                        if candidate['metadata']['form'] != selected_item['metadata']['form']:
                            # Check if forms are significantly different
                            form_pairs = [
                                ('bar', 'powder'), ('bar', 'cup'), ('bar', 'whole'),
                                ('powder', 'cup'), ('powder', 'whole'), ('cup', 'whole')
                            ]
                            if (candidate['metadata']['form'], selected_item['metadata']['form']) in form_pairs:
                                similarities.append(0.01)  # Very small diversity bonus
                            else:
                                similarities.append(0.0)
                        else:
                            similarities.append(0.0)  # No penalty for same form
                    diversity = 1 - max(similarities) if similarities else 0.0

                # MMR score (heavily weighted toward relevance)
                mmr_score = lambda_param * relevance + (1 - lambda_param) * diversity
                mmr_scores.append((mmr_score, candidate))

            # Select item with highest MMR score
            mmr_scores.sort(key=lambda x: x[0], reverse=True)
            selected.append(mmr_scores[0][1])
            remaining = [item[1] for item in mmr_scores[1:]]

        return selected

    def rebuild_from_database(self, db: Session):
        """
        Rebuild vector store from all products in database.

        Args:
            db: Database session
        """
        print("Rebuilding product vector store from database...")

        # Clear existing vector store
        self._create_vectorstore()

        # Get all products
        products = db.query(Product).all()
        print(f"Found {len(products)} products to index")

        # Add each product
        for i, product in enumerate(products):
            try:
                self.add_product_embedding(product)
                if (i + 1) % 100 == 0:
                    print(f"Indexed {i + 1} products")
            except Exception as e:
                print(f"Error indexing product {product.id}: {e}")

        # Commit embedding updates to database
        db.commit()
        print(f"Successfully indexed {len(products)} products")

# Global instance
_product_vector_store = None

def get_product_vector_store() -> ProductVectorStore:
    """
    Get or create the global product vector store instance.
    """
    global _product_vector_store
    if _product_vector_store is None:
        _product_vector_store = ProductVectorStore()
    return _product_vector_store

def add_product_embedding(product_id: int, db: Session):
    """
    Convenience function to add a product embedding.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        vector_store = get_product_vector_store()
        vector_store.add_product_embedding(product)

def query_similar_products(query_embedding: List[float], top_k: int = 10) -> List[int]:
    """
    Legacy function for backward compatibility.
    Use query_similar_products() method instead.
    This is a simplified version - use the full method for better results
    """
    vector_store = get_product_vector_store()
    results = vector_store.query_similar_products(
        query="",  # Would need to decode embedding to text
        top_k=top_k
    )
    return [result['product_id'] for result in results] 