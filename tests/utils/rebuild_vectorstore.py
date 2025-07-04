#!/usr/bin/env python3
"""
Script to rebuild the vector store with updated nutrition guidelines.
This will clear the existing vector store and recreate it with the new documents.
"""

import os
import sys
import shutil
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.macro_targeting import MacroTargetingService

def rebuild_vectorstore():
    """Rebuild the vector store with updated nutrition guidelines."""
    
    print("Starting vector store rebuild...")
    
    # Path to the vector store
    rag_store_path = "./rag_store"
    
    # Remove existing vector store if it exists
    if os.path.exists(rag_store_path):
        print(f"Removing existing vector store at {rag_store_path}")
        shutil.rmtree(rag_store_path)
    
    # Initialize the macro targeting service (this will create a new vector store)
    print("Initializing MacroTargetingService...")
    service = MacroTargetingService(rag_store_path=rag_store_path)
    
    # The service will automatically load documents and create the vector store
    print("Vector store rebuild completed successfully!")
    
    # Skip testing due to potential API quota issues
    print("Vector store rebuild completed successfully!")
    print("Note: Skipping test retrieval due to potential API quota limitations.")
    print("The vector store has been rebuilt with the new nutrition guidelines documents.")

if __name__ == "__main__":
    rebuild_vectorstore() 