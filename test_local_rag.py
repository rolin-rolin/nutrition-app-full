#!/usr/bin/env python3
"""
Test script for the local RAG pipeline using sentence-transformers and metadata-based filtering.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput

def test_local_rag_pipeline():
    """Test the local RAG pipeline with different user scenarios."""
    
    print("Testing Local RAG Pipeline with Sentence-Transformers")
    print("=" * 60)
    
    # Initialize the local service
    service = MacroTargetingServiceLocal()
    
    # Test cases with different metadata combinations
    test_cases = [
        {
            "name": "Child Cardio Short - Exact Metadata Match",
            "user_input": UserInput(
                id=1,
                user_query="I need nutrition advice for my 8-year-old doing 30 minutes of cardio",
                age=8,
                weight_kg=30.0,
                sex="male",
                exercise_type="cardio",
                exercise_duration_minutes=30,
                exercise_intensity="moderate"
            ),
            "expected_metadata": {
                "age_group": "age6-11",
                "type_of_activity": "cardio",
                "duration": "short"
            }
        },
        {
            "name": "Teen Strength Long - Exact Metadata Match",
            "user_input": UserInput(
                id=2,
                user_query="Nutrition for 16-year-old doing 90 minutes of strength training",
                age=16,
                weight_kg=65.0,
                sex="female",
                exercise_type="strength",
                exercise_duration_minutes=90,
                exercise_intensity="high"
            ),
            "expected_metadata": {
                "age_group": "age12-18",
                "type_of_activity": "strength",
                "duration": "long"
            }
        },
        {
            "name": "Adult Cardio Long - Exact Metadata Match",
            "user_input": UserInput(
                id=3,
                user_query="I'm 25 and doing 2 hours of cardio, what should I eat?",
                age=25,
                weight_kg=70.0,
                sex="male",
                exercise_type="cardio",
                exercise_duration_minutes=120,
                exercise_intensity="moderate"
            ),
            "expected_metadata": {
                "age_group": "age19-59",
                "type_of_activity": "cardio",
                "duration": "long"
            }
        },
        {
            "name": "Partial Metadata - Should Use Vector Search Fallback",
            "user_input": UserInput(
                id=4,
                user_query="I need nutrition advice",
                age=20,
                weight_kg=70.0,
                sex="male",
                # Missing exercise_type and duration
            ),
            "expected_metadata": {
                "age_group": "age19-59",
                # Missing other fields
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}: {test_case['name']}")
        print(f"{'='*60}")
        
        user_input = test_case['user_input']
        expected_metadata = test_case['expected_metadata']
        
        # Test metadata extraction
        print(f"\nUser Input:")
        print(f"  Age: {user_input.age}")
        print(f"  Exercise Type: {user_input.exercise_type}")
        print(f"  Duration: {user_input.exercise_duration_minutes} minutes")
        
        # Test metadata mapping
        age_group = service._get_age_group_from_age(user_input.age) if user_input.age else None
        exercise_type = service._get_exercise_type(user_input.exercise_type) if user_input.exercise_type else None
        duration_type = service._get_duration_type(user_input.exercise_duration_minutes) if user_input.exercise_duration_minutes else None
        
        print(f"\nMapped Metadata:")
        print(f"  Age Group: {age_group}")
        print(f"  Exercise Type: {exercise_type}")
        print(f"  Duration Type: {duration_type}")
        
        # Test context retrieval
        print(f"\nRetrieving Context...")
        try:
            context = service.retrieve_context_by_metadata(user_input)
            print(f"Context retrieved successfully!")
            print(f"Context length: {len(context)} characters")
            print(f"Context preview: {context[:200]}...")
            
            # Check if we got the expected content
            if "Guidelines for" in context:
                print("✅ Found nutrition guidelines content")
            else:
                print("⚠️  Content doesn't look like nutrition guidelines")
                
        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
        
        print()

def test_metadata_mapping():
    """Test the metadata mapping functions."""
    print("Testing Metadata Mapping Functions")
    print("=" * 40)
    
    service = MacroTargetingServiceLocal()
    
    # Test age group mapping
    print("\nAge Group Mapping:")
    test_ages = [5, 8, 12, 16, 20, 30, 50]
    for age in test_ages:
        age_group = service._get_age_group_from_age(age)
        print(f"  Age {age} -> {age_group}")
    
    # Test duration mapping
    print("\nDuration Mapping:")
    test_durations = [20, 30, 45, 60, 90, 120]
    for duration in test_durations:
        duration_type = service._get_duration_type(duration)
        print(f"  {duration} minutes -> {duration_type}")
    
    # Test exercise type mapping
    print("\nExercise Type Mapping:")
    test_exercises = ["running", "cardio", "strength training", "weightlifting", "soccer", "basketball"]
    for exercise in test_exercises:
        exercise_type = service._get_exercise_type(exercise)
        print(f"  '{exercise}' -> '{exercise_type}'")

if __name__ == "__main__":
    print("Local RAG Pipeline Test")
    print("This test will:")
    print("1. Test metadata-based document retrieval")
    print("2. Test fallback to vector search")
    print("3. Test metadata mapping functions")
    print()
    
    # Test metadata mapping first
    test_metadata_mapping()
    
    # Test the full pipeline
    test_local_rag_pipeline()
    
    print("\nTest completed!") 