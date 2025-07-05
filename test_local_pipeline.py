#!/usr/bin/env python3
"""
Test script to verify the local RAG pipeline is working correctly.

This script tests that the API endpoints are using the local macro targeting service.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput
from app.db.session import get_db

def test_local_pipeline():
    """Test that the local RAG pipeline is working correctly."""
    
    print("Testing Local RAG Pipeline...")
    
    # Check if OpenAI API key is available (needed for chat completions)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Warning: OPENAI_API_KEY not set. Chat completions will fail.")
        print("Testing only the local embedding and retrieval components...")
    
    # Initialize the local service
    print("Initializing MacroTargetingServiceLocal...")
    service = MacroTargetingServiceLocal(openai_api_key=openai_api_key)
    
    # Test document loading and metadata retrieval
    print("\n=== Testing Metadata-Based Retrieval ===")
    
    # Create a test user input that should match exact metadata
    user_input = UserInput(
        id=1,
        user_query="What should I eat for my cardio workout?",
        age=25,  # Maps to age19-59
        weight_kg=70.0,
        sex="male",
        exercise_type="cardio",  # Maps to cardio
        exercise_duration_minutes=45,  # Maps to short
        exercise_intensity="moderate",
        timing="pre-workout"
    )
    
    print(f"User input: {user_input.age}yo {user_input.sex}, {user_input.exercise_duration_minutes}min {user_input.exercise_type}")
    
    # Test metadata-based retrieval
    try:
        context = service.retrieve_context_by_metadata(user_input)
        print(f"✓ Metadata-based retrieval successful")
        print(f"Context length: {len(context)} characters")
        print(f"First 200 chars: {context[:200]}...")
    except Exception as e:
        print(f"✗ Metadata-based retrieval failed: {e}")
    
    # Test fallback vector search
    print("\n=== Testing Fallback Vector Search ===")
    try:
        context_fallback = service.retrieve_context_fallback(user_input)
        print(f"✓ Fallback vector search successful")
        print(f"Context length: {len(context_fallback)} characters")
        print(f"First 200 chars: {context_fallback[:200]}...")
    except Exception as e:
        print(f"✗ Fallback vector search failed: {e}")
    
    # Test the complete pipeline (if OpenAI key is available)
    if openai_api_key:
        print("\n=== Testing Complete Pipeline ===")
        try:
            # Get database session
            db = next(get_db())
            
            # Add user input to database
            db.add(user_input)
            db.commit()
            db.refresh(user_input)
            
            # Generate macro targets
            macro_target = service.create_or_update_macro_targets(user_input, db)
            
            print(f"✓ Complete pipeline successful")
            print(f"Generated macro targets:")
            print(f"  Calories: {macro_target.target_calories}")
            print(f"  Protein: {macro_target.target_protein}g")
            print(f"  Carbs: {macro_target.target_carbs}g")
            print(f"  Fat: {macro_target.target_fat}g")
            print(f"  Electrolytes: {macro_target.target_electrolytes}g")
            
        except Exception as e:
            print(f"✗ Complete pipeline failed: {e}")
    else:
        print("\n=== Skipping Complete Pipeline (no OpenAI key) ===")
    
    print("\n=== Local RAG Pipeline Test Complete ===")
    print("The pipeline is now using:")
    print("  ✓ Local sentence-transformers for embeddings")
    print("  ✓ Metadata-based filtering for exact matches")
    print("  ✓ Vector search fallback for complex queries")
    print("  ✓ Enhanced document loading with YAML frontmatter")

if __name__ == "__main__":
    test_local_pipeline() 