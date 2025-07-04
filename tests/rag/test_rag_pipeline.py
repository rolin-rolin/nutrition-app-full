#!/usr/bin/env python3
"""
Test script to verify the RAG pipeline with the new nutrition guidelines.
This script tests the complete flow from user input to context retrieval.
"""

import pytest

# Mark all tests in this file as RAG tests
pytestmark = pytest.mark.rag

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.macro_targeting import MacroTargetingService
from app.db.models import UserInput

def test_rag_pipeline():
    """Test the RAG pipeline with sample user inputs."""
    
    print("Testing RAG pipeline with nutrition guidelines...")
    
    # Initialize the service
    service = MacroTargetingService()
    
    # Test cases with different age groups and exercise types
    test_cases = [
        {
            "name": "Child Cardio Short",
            "user_input": UserInput(
                id=1,
                user_query="I need nutrition advice for my 8-year-old doing 30 minutes of cardio",
                age=8,
                weight_kg=30.0,
                sex="male",
                exercise_type="cardio",
                exercise_duration_minutes=30,
                exercise_intensity="moderate"
            )
        },
        {
            "name": "Teen Strength Long",
            "user_input": UserInput(
                id=2,
                user_query="Nutrition for 16-year-old doing 90 minutes of strength training",
                age=16,
                weight_kg=65.0,
                sex="female",
                exercise_type="strength",
                exercise_duration_minutes=90,
                exercise_intensity="high"
            )
        },
        {
            "name": "Adult Cardio Long",
            "user_input": UserInput(
                id=3,
                user_query="I'm 25 and doing 2 hours of cardio, what should I eat?",
                age=25,
                weight_kg=70.0,
                sex="male",
                exercise_type="cardio",
                exercise_duration_minutes=120,
                exercise_intensity="moderate"
            )
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {test_case['name']}")
        print(f"{'='*50}")
        
        user_input = test_case['user_input']
        
        # Build the query
        query = service._build_user_query(user_input)
        print(f"Generated query: {query}")
        
        # Retrieve context
        try:
            context = service.retrieve_context(query, k=2)
            print(f"\nRetrieved context (first 300 chars):")
            print(f"{context[:300]}...")
            
            # Show which documents were retrieved
            print(f"\nContext length: {len(context)} characters")
            
        except Exception as e:
            print(f"Error retrieving context: {e}")
        
        print()

if __name__ == "__main__":
    test_rag_pipeline() 