"""
Global singleton for SentenceTransformer model to ensure only one instance is loaded.
"""
from typing import Optional
from sentence_transformers import SentenceTransformer
import gc
import weakref

class GlobalEmbeddings:
    _instance = None
    _model: Optional[SentenceTransformer] = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def model(self) -> SentenceTransformer:
        """Lazy load the model only when needed."""
        if self._model is None:
            print("[DEBUG] Loading SentenceTransformer model...")
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
            # Create a weakref to help with garbage collection
            weakref.finalize(self._model, self._cleanup_model)
        return self._model
    
    @classmethod
    def _cleanup_model(cls):
        """Cleanup function called when model is garbage collected."""
        print("[DEBUG] Cleaning up SentenceTransformer model...")
        if cls._model is not None:
            del cls._model
            cls._model = None
            gc.collect()

def get_embedding_model() -> SentenceTransformer:
    """Get the global embedding model instance."""
    return GlobalEmbeddings.get_instance().model
