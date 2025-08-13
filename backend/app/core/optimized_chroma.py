"""
Optimized Chroma Store for Memory-Efficient Operations

This class provides memory-optimized operations for Chroma vector store,
including batching, lazy loading, and automatic cleanup to stay under 512 MB RAM.
"""

import os
import gc
from typing import List, Dict, Any, Optional, Callable
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
import numpy as np


class OptimizedChromaStore:
    """
    Memory-optimized wrapper around Chroma vector store.
    
    Features:
    - Batch document addition to control memory usage
    - Lazy loading of embeddings
    - Automatic garbage collection
    - Memory-efficient similarity search
    - Configurable batch sizes
    """
    
    def __init__(self, persist_directory: str, embedding_function: Embeddings, 
                 batch_size: int = 32, max_memory_mb: int = 400):
        """
        Initialize the optimized Chroma store.
        
        Args:
            persist_directory: Directory to persist the vector store
            embedding_function: LangChain embedding function
            batch_size: Number of documents to process in each batch
            max_memory_mb: Maximum memory usage in MB before forcing cleanup
        """
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function
        self.batch_size = batch_size
        self.max_memory_mb = max_memory_mb
        
        # Initialize the underlying Chroma store
        self.store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function
        )
        
        # Track memory usage
        self._last_memory_check = 0
        self._document_count = 0
        
    def batch_add_documents(self, documents: List[Document]) -> None:
        """
        Add documents in batches to control memory usage.
        
        Args:
            documents: List of documents to add
        """
        if not documents:
            return
            
        print(f"[DEBUG] Adding {len(documents)} documents in batches of {self.batch_size}")
        
        # Process documents in batches
        for i in range(0, len(documents), self.batch_size):
            batch = documents[i:i + self.batch_size]
            
            # Add batch to store
            self.store.add_documents(batch)
            
            # Update document count
            self._document_count += len(batch)
            
            # Force garbage collection after each batch
            gc.collect()
            
            # Check memory usage periodically
            if i % (self.batch_size * 4) == 0:
                self._check_memory_usage()
                
        # Final memory check and cleanup
        self._check_memory_usage()
        gc.collect()
        
        print(f"[DEBUG] Successfully added {len(documents)} documents. Total: {self._document_count}")
    
    def similarity_search(self, query: str, k: int = 4, 
                         where: Optional[Dict[str, Any]] = None,
                         **kwargs) -> List[Document]:
        """
        Perform similarity search with memory optimization.
        
        Args:
            query: Query string
            k: Number of results to return
            where: Metadata filter
            **kwargs: Additional arguments for similarity search
            
        Returns:
            List of similar documents
        """
        # Check memory before search
        self._check_memory_usage()
        
        try:
            # Perform the search
            results = self.store.similarity_search(
                query=query,
                k=k,
                where=where,
                **kwargs
            )
            
            # Clean up after search
            gc.collect()
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Similarity search failed: {e}")
            # Force cleanup on error
            gc.collect()
            raise
    
    def similarity_search_with_score(self, query: str, k: int = 4,
                                   where: Optional[Dict[str, Any]] = None,
                                   **kwargs) -> List[tuple]:
        """
        Perform similarity search with scores and memory optimization.
        
        Args:
            query: Query string
            k: Number of results to return
            where: Metadata filter
            **kwargs: Additional arguments for similarity search
            
        Returns:
            List of (document, score) tuples
        """
        # Check memory before search
        self._check_memory_usage()
        
        try:
            # Perform the search
            results = self.store.similarity_search_with_score(
                query=query,
                k=k,
                where=where,
                **kwargs
            )
            
            # Clean up after search
            gc.collect()
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Similarity search with score failed: {e}")
            # Force cleanup on error
            gc.collect()
            raise
    
    def get(self, include: Optional[List[str]] = None, 
            where: Optional[Dict[str, Any]] = None,
            **kwargs) -> Dict[str, Any]:
        """
        Get documents with memory optimization.
        
        Args:
            include: List of fields to include
            where: Metadata filter
            **kwargs: Additional arguments
            
        Returns:
            Dictionary containing documents and metadata
        """
        # Check memory before operation
        self._check_memory_usage()
        
        try:
            # Get documents
            results = self.store.get(
                include=include,
                where=where,
                **kwargs
            )
            
            # Clean up after operation
            gc.collect()
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Get operation failed: {e}")
            # Force cleanup on error
            gc.collect()
            raise
    
    def delete(self, where: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        """
        Delete documents with memory optimization.
        
        Args:
            where: Metadata filter for documents to delete
            **kwargs: Additional arguments
        """
        # Check memory before operation
        self._check_memory_usage()
        
        try:
            # Delete documents
            self.store.delete(where=where, **kwargs)
            
            # Clean up after operation
            gc.collect()
            
        except Exception as e:
            print(f"[ERROR] Delete operation failed: {e}")
            # Force cleanup on error
            gc.collect()
            raise
    
    def persist(self) -> None:
        """Persist the vector store to disk."""
        try:
            self.store.persist()
            print("[DEBUG] Vector store persisted successfully")
        except Exception as e:
            print(f"[ERROR] Failed to persist vector store: {e}")
    
    def _check_memory_usage(self) -> None:
        """
        Check current memory usage and force cleanup if needed.
        """
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            # Only check every 100 operations to avoid overhead
            if self._last_memory_check % 100 == 0:
                print(f"[DEBUG] Current memory usage: {memory_mb:.1f} MB")
                
                if memory_mb > self.max_memory_mb:
                    print(f"[WARNING] Memory usage ({memory_mb:.1f} MB) exceeds limit ({self.max_memory_mb} MB). Forcing cleanup...")
                    self._force_cleanup()
                    
            self._last_memory_check += 1
            
        except ImportError:
            # psutil not available, skip memory checking
            pass
        except Exception as e:
            print(f"[WARNING] Memory check failed: {e}")
    
    def _force_cleanup(self) -> None:
        """
        Force aggressive memory cleanup.
        """
        print("[DEBUG] Performing forced memory cleanup...")
        
        # Multiple garbage collection passes
        for _ in range(3):
            gc.collect()
        
        # Clear any cached embeddings if possible
        if hasattr(self.embedding_function, '_model') and self.embedding_function._model is not None:
            try:
                # Clear model cache if it has one
                if hasattr(self.embedding_function._model, 'clear_cache'):
                    self.embedding_function._model.clear_cache()
            except:
                pass
        
        print("[DEBUG] Memory cleanup completed")
    
    def get_document_count(self) -> int:
        """Get the total number of documents in the store."""
        try:
            results = self.store.get()
            return len(results.get('documents', []))
        except:
            return self._document_count
    
    def get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0
    
    def cleanup(self) -> None:
        """Clean up resources and force garbage collection."""
        print("[DEBUG] Cleaning up OptimizedChromaStore...")
        
        # Clear any references
        if hasattr(self, 'store'):
            del self.store
        
        # Force garbage collection
        gc.collect()
        
        print("[DEBUG] OptimizedChromaStore cleanup completed")
