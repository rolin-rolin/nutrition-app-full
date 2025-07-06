#!/usr/bin/env python3
"""
Test script for the Macro Targets API endpoint.

This script tests the /macro-targets/ endpoint with various user inputs.
"""

import requests
import json
import time
from typing import Dict, Any

def test_macro_targets_api():
    """Test the macro targets API endpoint."""
    
    base_url = "http://localhost:8000"
    
    # Test cases with different user inputs
    test_cases = [
        {
            "name": "Adult Cardio Short Session",
            "data": {
                "user_query": "What should I eat for my 45-minute cardio workout?",
                "age": 25,
                "weight_kg": 70.0,
                "sex": "male",
                "exercise_type": "cardio",
                "exercise_duration_minutes": 45,
                "exercise_intensity": "moderate",
                "timing": "pre-workout"
            }
        },
        {
            "name": "Teen Strength Long Session",
            "data": {
                "user_query": "Nutrition advice for my 90-minute strength training session",
                "age": 16,
                "weight_kg": 65.0,
                "sex": "female",
                "exercise_type": "strength",
                "exercise_duration_minutes": 90,
                "exercise_intensity": "high",
                "timing": "post-workout"
            }
        },
        {
            "name": "Child Cardio Short Session",
            "data": {
                "user_query": "What should my 10-year-old eat for soccer practice?",
                "age": 10,
                "weight_kg": 35.0,
                "sex": "male",
                "exercise_type": "soccer",
                "exercise_duration_minutes": 30,
                "exercise_intensity": "moderate",
                "timing": "general"
            }
        }
    ]
    
    print("=== Testing Macro Targets API ===\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        print("✓ API server is running")
    except requests.exceptions.RequestException as e:
        print(f"✗ API server is not running: {e}")
        print("Please start the server with: uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        return
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['name']} ---")
        
        try:
            # Make API request
            response = requests.post(
                f"{base_url}/api/v1/macro-targets/",
                json=test_case['data'],
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✓ API call successful!")
                print(f"Generated Macro Targets:")
                print(f"  Calories: {result.get('target_calories')}")
                print(f"  Protein: {result.get('target_protein')}g")
                print(f"  Carbs: {result.get('target_carbs')}g")
                print(f"  Fat: {result.get('target_fat')}g")
                print(f"  Electrolytes: {result.get('target_electrolytes')}g")
                
                # Show timing breakdown if available
                if result.get('pre_workout_macros'):
                    print(f"  Pre-workout: {result['pre_workout_macros']}")
                if result.get('during_workout_macros'):
                    print(f"  During workout: {result['during_workout_macros']}")
                if result.get('post_workout_macros'):
                    print(f"  Post-workout: {result['post_workout_macros']}")
                
                print(f"  RAG Context length: {len(result.get('rag_context', ''))} characters")
                print(f"  Reasoning length: {len(result.get('reasoning', ''))} characters")
                
            else:
                print(f"✗ API call failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")
        except json.JSONDecodeError as e:
            print(f"✗ JSON decode error: {e}")
            print(f"Response text: {response.text}")
    
    print("\n=== API Testing Complete ===")

def test_api_documentation():
    """Test if the API documentation is accessible."""
    
    print("\n=== Testing API Documentation ===")
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✓ API documentation is accessible at http://localhost:8000/docs")
        else:
            print(f"✗ API documentation returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot access API documentation: {e}")

if __name__ == "__main__":
    test_api_documentation()
    test_macro_targets_api() 