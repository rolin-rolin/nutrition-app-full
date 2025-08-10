#!/usr/bin/env python3
"""
Minimal test: load documents, create Chroma vector store, print all stored metadata.
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.macro_targeting_local import MacroTargetingServiceLocal
from langchain_chroma import Chroma

if __name__ == "__main__":
    print("Minimal Chroma test: loader + vector store + metadata print\n")
    service = MacroTargetingServiceLocal()
    documents = service._load_documents()
    print(f"Loaded {len(documents)} documents from loader.")

    # Remove any existing vector store
    if os.path.exists("data/rag_store"):
        import shutil
        shutil.rmtree("data/rag_store")

    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents,
        embedding=service._get_embedding_function(),
        persist_directory="data/rag_store"
    )
    # vectorstore.persist()  # Not needed in langchain_chroma

    # Query all documents and print metadata
    results = vectorstore.get(include=["documents", "metadatas"])
    print(f"\nChroma now holds {len(results['documents'])} documents.")
    for i, metadata in enumerate(results['metadatas']):
        print(f"  Doc {i}: {metadata}")
    print("\nDone.") 