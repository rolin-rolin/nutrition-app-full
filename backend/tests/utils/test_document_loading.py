#!/usr/bin/env python3
"""
Test script to verify document loading from nutrition guidelines.
This script tests the document loading without making API calls.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def test_document_loading():
    """Test loading documents from nutrition guidelines directory."""
    
    print("Testing document loading from nutrition guidelines...")
    
    documents = []
    guidelines_dir = "nutrition_guidelines"
    
    # Age groups and their corresponding directories
    age_groups = ["age6-11", "age12-18", "age19-59"]
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    for age_group in age_groups:
        age_group_path = os.path.join(guidelines_dir, age_group)
        if not os.path.exists(age_group_path):
            print(f"Warning: Age group directory {age_group_path} does not exist")
            continue
            
        # Load all .md files in the age group directory
        try:
            for filename in os.listdir(age_group_path):
                if filename.endswith('.md'):
                    filepath = os.path.join(age_group_path, filename)
                    try:
                        loader = TextLoader(filepath)
                        docs = loader.load()
                        # Add metadata to help with retrieval
                        for doc in docs:
                            doc.metadata.update({
                                'age_group': age_group,
                                'filename': filename,
                                'filepath': filepath
                            })
                        documents.extend(splitter.split_documents(docs))
                        print(f"Loaded: {filepath}")
                    except Exception as e:
                        print(f"Warning: Could not load {filepath}: {e}")
        except Exception as e:
            print(f"Warning: Could not access directory {age_group_path}: {e}")
    
    print(f"Total documents loaded: {len(documents)}")
    
    # Print some sample document information
    if documents:
        print("\nSample document information:")
        for i, doc in enumerate(documents[:3]):  # Show first 3 documents
            print(f"Document {i+1}:")
            print(f"  Age group: {doc.metadata.get('age_group', 'N/A')}")
            print(f"  Filename: {doc.metadata.get('filename', 'N/A')}")
            print(f"  Content preview: {doc.page_content[:100]}...")
            print()
    
    return documents

if __name__ == "__main__":
    test_document_loading() 