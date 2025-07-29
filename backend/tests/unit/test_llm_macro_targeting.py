#!/usr/bin/env python3
"""
Test script for LLM-enhanced macro targeting service.

This script demonstrates the new functionality that extracts structured fields
from natural language user queries using OpenAI's API and generates macro targets.
"""

import os
import sys
from pathlib import Path

# Add the backend app to the Python path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from dotenv import load_dotenv
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.session import SessionLocal

load_dotenv()

def test_llm_field_extraction():
    """Test the LLM field extraction functionality."""
    
    # Check if OpenAI API key is available
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    print("=== Testing LLM Field Extraction ===\n")
    
    # Initialize the service
    service = MacroTargetingServiceLocal(openai_api_key=openai_api_key)
    
    # Test queries
    test_queries = [
        "I'm an 18-year-old guy, weigh 160 pounds. I want savory, chewy snacks for my 90-minute soccer match to fuel recovery. I'm lactose intolerant and I'd like to be gluten-free. Keep it under 400 calories",
        "I'm 25 years old, 140 lbs. Going to the gym for 45 minutes of weightlifting. I want sweet, crunchy snacks. I'm vegan and allergic to nuts.",
        "Need pre-workout fuel for my 2-hour cycling session. I'm 30, weigh 170 pounds. Looking for fruity flavors, smooth texture. No dairy please, budget is $10.",
        "22-year-old female, 125 pounds. 60-minute HIIT workout. Want chocolate flavor, prefer organic options."
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test Query {i}:")
        print(f"Input: {query}")
        print()
        
        # Extract fields using LLM
        extracted_fields = service.extract_fields_from_query(query)
        print("Extracted Fields:")
        print(f"  Age: {extracted_fields.get('age')}")
        print(f"  Weight (lbs): {extracted_fields.get('weight_lb')}")
        print(f"  Activity Type: {extracted_fields.get('activity_type')}")
        print(f"  Duration (min): {extracted_fields.get('duration_minutes')}")
        print(f"  Calorie Cap: {extracted_fields.get('calorie_cap')}")
        print(f"  Soft Preferences: {extracted_fields.get('soft_preferences')}")
        print(f"  Hard Constraints: {extracted_fields.get('hard_filters')}")
        print()
        
        # Convert to UserInput format
        user_input_data = service._convert_extracted_fields_to_user_input(extracted_fields, query)
        print("Converted UserInput Data:")
        print(f"  Age: {user_input_data.get('age')}")
        print(f"  Weight (kg): {user_input_data.get('weight_kg')}")
        print(f"  Exercise Type: {user_input_data.get('exercise_type')}")
        print(f"  Duration (min): {user_input_data.get('exercise_duration_minutes')}")
        print(f"  Preferences: {user_input_data.get('preferences')}")
        print()
        print("-" * 80)
        print()

def test_full_pipeline():
    """Test the complete pipeline from query to macro targets."""
    
    # Check if OpenAI API key is available
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: Please set your OPENAI_API_KEY environment variable")
        return
    
    print("=== Testing Complete Pipeline ===\n")
    
    # Initialize the service
    service = MacroTargetingServiceLocal(openai_api_key=openai_api_key)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Test query
        test_query = "I'm an 18-year-old guy, weigh 160 pounds. I want savory, chewy snacks for my 90-minute soccer match to fuel recovery. I'm lactose intolerant and I'd like to be gluten-free. Keep it under 400 calories"
        
        print(f"Test Query: {test_query}")
        print()
        
        # Generate macro targets from query
        user_input, macro_target = service.generate_macro_targets_from_query(test_query, db)
        
        print("Generated UserInput:")
        print(f"  ID: {user_input.id}")
        print(f"  Age: {user_input.age}")
        print(f"  Weight (kg): {user_input.weight_kg}")
        print(f"  Exercise Type: {user_input.exercise_type}")
        print(f"  Duration (min): {user_input.exercise_duration_minutes}")
        print(f"  Preferences: {user_input.preferences}")
        print()
        
        print("Generated Macro Targets:")
        print(f"  ID: {macro_target.id}")
        print(f"  Target Calories: {macro_target.target_calories:.1f}")
        print(f"  Target Protein: {macro_target.target_protein:.1f}g")
        print(f"  Target Carbs: {macro_target.target_carbs:.1f}g")
        print(f"  Target Fat: {macro_target.target_fat:.1f}g")
        print(f"  Target Electrolytes: {macro_target.target_electrolytes:.1f}mg")
        print()
        
        print("Timing Breakdown:")
        print(f"  Pre-workout: {macro_target.pre_workout_macros}")
        print(f"  During-workout: {macro_target.during_workout_macros}")
        print(f"  Post-workout: {macro_target.post_workout_macros}")
        print()
        
        print(f"Reasoning: {macro_target.reasoning}")
        print()
        
        print("RAG Context (first 200 chars):")
        print(f"{macro_target.rag_context[:200]}...")
        
    except Exception as e:
        print(f"Error in full pipeline test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()

def test_fallback_extraction():
    """Test the fallback field extraction when OpenAI is not available."""
    
    print("=== Testing Fallback Field Extraction ===\n")
    
    # Initialize service without OpenAI key
    service = MacroTargetingServiceLocal(openai_api_key=None)
    
    # Test query
    test_query = "I'm 20 years old, weigh 150 pounds. Going for a 60-minute run. Want 300 calories max."
    
    print(f"Test Query: {test_query}")
    print()
    
    # Extract fields using fallback method
    extracted_fields = service.extract_fields_from_query(test_query)
    print("Fallback Extracted Fields:")
    print(f"  Age: {extracted_fields.get('age')}")
    print(f"  Weight (lbs): {extracted_fields.get('weight_lb')}")
    print(f"  Activity Type: {extracted_fields.get('activity_type')}")
    print(f"  Duration (min): {extracted_fields.get('duration_minutes')}")
    print(f"  Calorie Cap: {extracted_fields.get('calorie_cap')}")
    print(f"  Soft Preferences: {extracted_fields.get('soft_preferences')}")
    print(f"  Hard Constraints: {extracted_fields.get('hard_filters')}")

if __name__ == "__main__":
    print("LLM-Enhanced Macro Targeting Service Test")
    print("=========================================\n")
    
    # Test field extraction
    test_llm_field_extraction()
    
    # Test fallback extraction
    test_fallback_extraction()
    
    # Test complete pipeline
    test_full_pipeline()
    
    print("\nTest completed!") 