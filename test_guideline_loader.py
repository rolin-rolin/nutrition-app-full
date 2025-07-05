#!/usr/bin/env python3
"""
Test script to verify guideline document loading and metadata extraction.
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from app.core.macro_targeting_local import MacroTargetingServiceLocal

if __name__ == "__main__":
    print("Testing guideline document loader...")
    service = MacroTargetingServiceLocal()
    documents = service._load_documents()
    print(f"\nLoaded {len(documents)} documents.")
    for i, doc in enumerate(documents):
        print(f"\nDocument {i}:")
        print(f"  Metadata: {doc.metadata}")
        print(f"  Content preview: {doc.page_content[:100]}...")
    print("\nDone.") 