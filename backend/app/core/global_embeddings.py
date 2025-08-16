"""
Global singleton for SentenceTransformer model to ensure only one instance is loaded.
"""
from typing import Optional
import gc
import weakref

class GlobalEmbeddings:
    _instance = None
    _model: Optional[object] = None  # Using object to avoid import at module level
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def model(self):
        """Lazy load the model only when needed."""
        if self._model is None:
            print("[DEBUG] Loading SentenceTransformer model...")
            # Lazy import to avoid loading heavy dependencies at startup
            from sentence_transformers import SentenceTransformer
            # Use device='cpu' to ensure CPU-only usage and reduce memory
            self._model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
            # Create a weakref to help with garbage collection
            weakref.finalize(self._model, self._cleanup_model)
        return self._model
    
    def encode_with_optimization(self, texts, **kwargs):
        """Encode texts with PyTorch memory optimizations."""
        import torch
        
        # Use no_grad context to prevent gradient computation and save memory
        with torch.no_grad():
            # Ensure we're using CPU
            if hasattr(self._model, 'device'):
                self._model.to('cpu')
            
            # Encode with memory-efficient settings
            embeddings = self._model.encode(texts, **kwargs)
            
            # Convert to CPU if needed and clear CUDA cache
            if hasattr(torch.cuda, 'empty_cache'):
                torch.cuda.empty_cache()
            
            # Force garbage collection
            gc.collect()
            
            return embeddings
    
    @classmethod
    def _cleanup_model(cls):
        """Cleanup function called when model is garbage collected."""
        print("[DEBUG] Cleaning up SentenceTransformer model...")
        if cls._model is not None:
            del cls._model
            cls._model = None
            gc.collect()
    
    @classmethod
    def clear_model(cls):
        """Explicitly clear the model to free memory."""
        if cls._model is not None:
            print("[DEBUG] Explicitly clearing SentenceTransformer model...")
            del cls._model
            cls._model = None
            gc.collect()

def get_embedding_model():
    """Get the global embedding model instance."""
    return GlobalEmbeddings.get_instance().model

def get_optimized_encoder():
    """Get the global embedding model with PyTorch optimizations."""
    return GlobalEmbeddings.get_instance().encode_with_optimization

def clear_embedding_model():
    """Clear the global embedding model to free memory."""
    GlobalEmbeddings.clear_model()
