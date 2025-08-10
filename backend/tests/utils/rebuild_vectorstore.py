#!/usr/bin/env python3
"""
Utility script to rebuild the vector store from nutrition guidelines.

This script can be used to:
1. Clear the existing vector store
2. Reload all nutrition guideline documents
3. Rebuild the embeddings and metadata
"""

import os
import sys
import shutil
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.macro_targeting_local import MacroTargetingServiceLocal

def rebuild_vectorstore(rag_store_path: str = "./data/rag_store"):
    """Rebuild the vector store from scratch."""
    
    print(f"Rebuilding vector store at: {rag_store_path}")
    
    # Remove existing vector store if it exists
    if os.path.exists(rag_store_path):
        print(f"Removing existing vector store: {rag_store_path}")
        shutil.rmtree(rag_store_path)
    
    # Initialize service to rebuild vector store
    print("Initializing MacroTargetingServiceLocal...")
    service = MacroTargetingServiceLocal(rag_store_path=rag_store_path, force_rebuild=True)
    
    print("Vector store rebuilt successfully!")
    print(f"Vector store location: {rag_store_path}")

if __name__ == "__main__":
    rebuild_vectorstore() 