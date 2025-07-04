#!/usr/bin/env python3
"""
Test script to demonstrate JSON output from GPT for macro targeting.

This script shows how GPT now returns structured JSON instead of free text.
"""

import pytest

# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration

import os
import json
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.macro_targeting import MacroTargetingService
from app.db.models import UserInput
from app.db.session import get_db

def test_json_output():
    """Test the JSON output functionality"""
    
    # Set your OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Please set your OPENAI_API_KEY environment variable")
        return
    
    # Initialize the service
    print("Testing JSON Output from GPT...")
    service = MacroTargetingService(openai_api_key=openai_api_key)
    
    # Create a test user input
    user_input = UserInput(
        user_query="What should I eat after my workout?",
        age=25,
        weight_kg=75.0,
        sex="male",
        exercise_type="weightlifting",
        exercise_duration_minutes=60,
        exercise_intensity="high",
        timing="post-workout"
    )
    
    # Generate macro targets
    macro_target = service.generate_macro_targets(user_input)
    
    print(f"\n=== GPT Response (JSON) ===")
    print(f"Raw response: {macro_target.reasoning}")
    
    print(f"\n=== Parsed Macro Targets ===")
    print(f"Calories: {macro_target.target_calories}")
    print(f"Protein: {macro_target.target_protein}g")
    print(f"Carbs: {macro_target.target_carbs}g")
    print(f"Fat: {macro_target.target_fat}g")
    print(f"Electrolytes: {macro_target.target_electrolytes}g")
    
    # Test JSON parsing directly
    print(f"\n=== JSON Parsing Test ===")
    try:
        parsed_json = json.loads(macro_target.reasoning)
        print("Successfully parsed JSON response")
        print(f"JSON structure: {list(parsed_json.keys())}")
    except json.JSONDecodeError as e:
        print(f" Failed to parse JSON: {e}")
        print("This might happen if GPT includes extra text outside the JSON")

if __name__ == "__main__":
    test_json_output() 