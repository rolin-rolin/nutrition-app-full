#!/usr/bin/env python3
"""
Script to rebuild the product vector store from the database.

This script will:
1. Load all products from the database
2. Generate embeddings for each product
3. Store them in the Chroma vector store
4. Update the database with embedding information

Usage:
    python rebuild_product_vectorstore.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.vector_store import get_product_vector_store
from app.db.models import Product

def main():
    print("Starting product vector store rebuild...")
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get vector store
        vector_store = get_product_vector_store()
        
        # Rebuild from database
        vector_store.rebuild_from_database(db)
        
        print("Product vector store rebuild completed successfully!")
        
    except Exception as e:
        print(f"Error rebuilding product vector store: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 