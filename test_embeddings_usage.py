#!/usr/bin/env python3
"""
Test script to demonstrate how sentence-transformers is used in the local RAG pipeline.

This script shows:
1. How sentence-transformers embeds documents during vector store creation
2. How sentence-transformers embeds queries during retrieval
3. The difference between metadata-based filtering and vector search
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput

def test_embeddings_usage():
    """Test and demonstrate how sentence-transformers is used."""
    
    print("=== Testing Sentence-Transformers Usage in Local RAG Pipeline ===\n")
    
    # Initialize the service
    print("1. Initializing MacroTargetingServiceLocal...")
    service = MacroTargetingServiceLocal()
    
    print(f"   ✓ SentenceTransformer model loaded: {service.embeddings}")
    print(f"   ✓ Model name: {service.embeddings.get_sentence_embedding_dimension()} dimensions")
    
    # Test embedding a sample document
    print("\n2. Testing document embedding...")
    sample_doc = "Guidelines for Cardio, Short Duration (20–30 min), Age 19–59. Total Carbs: 0.5–0.7 g/kg"
    doc_embedding = service.embeddings.encode([sample_doc])
    print(f"   ✓ Document embedded: {len(doc_embedding[0])} dimensions")
    print(f"   ✓ Sample embedding values: {doc_embedding[0][:5]}...")
    
    # Test embedding a sample query
    print("\n3. Testing query embedding...")
    sample_query = "I need nutrition advice for cardio workout"
    query_embedding = service.embeddings.encode([sample_query])
    print(f"   ✓ Query embedded: {len(query_embedding[0])} dimensions")
    print(f"   ✓ Sample embedding values: {query_embedding[0][:5]}...")
    
    # Test the embedding function wrapper
    print("\n4. Testing LangChain embedding function wrapper...")
    embedding_function = service._get_embedding_function()
    
    # Test document embedding through wrapper
    docs_embeddings = embedding_function.embed_documents([sample_doc])
    print(f"   ✓ Wrapper document embedding: {len(docs_embeddings[0])} dimensions")
    
    # Test query embedding through wrapper
    query_embedding_wrapper = embedding_function.embed_query(sample_query)
    print(f"   ✓ Wrapper query embedding: {len(query_embedding_wrapper)} dimensions")
    
    # Test vector store retrieval (this uses sentence-transformers)
    print("\n5. Testing vector store retrieval (uses sentence-transformers)...")
    
    # Create a test user input
    user_input = UserInput(
        id=999,  # Use a unique ID
        user_query="What should I eat for my cardio workout?",
        age=25,
        weight_kg=70.0,
        sex="male",
        exercise_type="cardio",
        exercise_duration_minutes=45,
        exercise_intensity="moderate",
        timing="pre-workout"
    )
    
    print(f"   Test user: {user_input.age}yo {user_input.sex}, {user_input.exercise_duration_minutes}min {user_input.exercise_type}")
    
    # Test metadata-based retrieval (does NOT use sentence-transformers)
    print("\n   a) Metadata-based retrieval (NO sentence-transformers):")
    try:
        context_metadata = service.retrieve_context_by_metadata(user_input)
        print(f"   ✓ Metadata retrieval successful: {len(context_metadata)} characters")
        print(f"   ✓ First 100 chars: {context_metadata[:100]}...")
    except Exception as e:
        print(f"   ✗ Metadata retrieval failed: {e}")
    
    # Test fallback vector search (DOES use sentence-transformers)
    print("\n   b) Fallback vector search (USES sentence-transformers):")
    try:
        context_vector = service.retrieve_context_fallback(user_input)
        print(f"   ✓ Vector search successful: {len(context_vector)} characters")
        print(f"   ✓ First 100 chars: {context_vector[:100]}...")
    except Exception as e:
        print(f"   ✗ Vector search failed: {e}")
    
    # Test direct vector search
    print("\n6. Testing direct vector search with sentence-transformers...")
    try:
        # This will use sentence-transformers to embed the query and find similar documents
        retriever = service.vectorstore.as_retriever(search_kwargs={"k": 1})
        results = retriever.get_relevant_documents("cardio exercise nutrition guidelines")
        
        if results:
            print(f"   ✓ Vector search found document: {len(results[0].page_content)} characters")
            print(f"   ✓ Document metadata: {results[0].metadata}")
        else:
            print("   ✗ No documents found")
    except Exception as e:
        print(f"   ✗ Vector search failed: {e}")
    
    print("\n=== Summary ===")
    print("Sentence-transformers is used in the following ways:")
    print("1. ✓ Document embedding: When creating the vector store, all nutrition guidelines are embedded")
    print("2. ✓ Query embedding: When doing vector search, user queries are embedded")
    print("3. ✓ Similarity search: Chroma uses the embeddings to find similar documents")
    print("4. ✗ Metadata filtering: Uses exact metadata matching, no embeddings needed")
    print("5. ✓ Fallback search: When metadata doesn't match, falls back to vector search with embeddings")
    
    print("\nThe vector store currently contains:")
    print(f"- {len(service.vectorstore.get()['documents'])} documents")
    print(f"- Each document has been embedded using sentence-transformers")
    print(f"- Embeddings are stored in: {service.rag_store_path}")

if __name__ == "__main__":
    test_embeddings_usage() 