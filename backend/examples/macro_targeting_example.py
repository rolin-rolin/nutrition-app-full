#!/usr/bin/env python3
"""
Example script demonstrating the RAG pipeline for macro targeting.

This script shows how to:
1. Initialize the macro targeting service
2. Create user inputs with context
3. Generate macro targets using the RAG pipeline
4. Store and retrieve results from the database
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput, MacroTarget
from app.db.session import get_db

def main():
    """Main example function"""
    
    # Set your OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Please set your OPENAI_API_KEY environment variable")
        return
    
    # Initialize the service
    print("Initializing Macro Targeting Service...")
    service = MacroTargetingServiceLocal(openai_api_key=openai_api_key)
    
    # Get database session
    db = next(get_db())
    
    # Example 1: Post-workout nutrition for a soccer player
    print("\n=== Example 1: Post-workout nutrition for soccer player ===")
    
    user_input_1 = UserInput(
        user_query="What should I eat to recover after my soccer game?",
        age=19,
        weight_kg=70.0,
        sex="male",
        exercise_type="soccer",
        exercise_duration_minutes=90,
        exercise_intensity="high",
        timing="post-workout"
    )
    
    db.add(user_input_1)
    db.commit()
    db.refresh(user_input_1)
    
    macro_target_1 = service.create_or_update_macro_targets(user_input_1, db)
    
    print(f"User Query: {user_input_1.user_query}")
    print(f"Context: {user_input_1.age}yo {user_input_1.sex}, {user_input_1.weight_kg}kg")
    print(f"Exercise: {user_input_1.exercise_duration_minutes}min {user_input_1.exercise_type}")
    print(f"\nMacro Targets:")
    print(f"  Calories: {macro_target_1.target_calories}")
    print(f"  Protein: {macro_target_1.target_protein}g")
    print(f"  Carbs: {macro_target_1.target_carbs}g")
    print(f"  Fat: {macro_target_1.target_fat}g")
    print(f"  Electrolytes: {macro_target_1.target_electrolytes}g")
    print(f"\nReasoning: {macro_target_1.reasoning[:200]}...")
    
    # Example 2: Pre-workout nutrition for a runner
    print("\n=== Example 2: Pre-workout nutrition for runner ===")
    
    user_input_2 = UserInput(
        user_query="What should I eat before my morning run?",
        age=28,
        weight_kg=65.0,
        sex="female",
        exercise_type="running",
        exercise_duration_minutes=45,
        exercise_intensity="medium",
        timing="pre-workout"
    )
    
    db.add(user_input_2)
    db.commit()
    db.refresh(user_input_2)
    
    macro_target_2 = service.create_or_update_macro_targets(user_input_2, db)
    
    print(f"User Query: {user_input_2.user_query}")
    print(f"Context: {user_input_2.age}yo {user_input_2.sex}, {user_input_2.weight_kg}kg")
    print(f"Exercise: {user_input_2.exercise_duration_minutes}min {user_input_2.exercise_type}")
    print(f"\nMacro Targets:")
    print(f"  Calories: {macro_target_2.target_calories}")
    print(f"  Protein: {macro_target_2.target_protein}g")
    print(f"  Carbs: {macro_target_2.target_carbs}g")
    print(f"  Fat: {macro_target_2.target_fat}g")
    print(f"  Electrolytes: {macro_target_2.target_electrolytes}g")
    print(f"\nReasoning: {macro_target_2.reasoning[:200]}...")
    
    # Example 3: Retrieve from history
    print("\n=== Example 3: Retrieving from history ===")
    
    # Get all macro targets from the database
    all_targets = db.query(MacroTarget).all()
    print(f"Total macro targets in database: {len(all_targets)}")
    
    for target in all_targets:
        user_input = db.query(UserInput).filter(UserInput.id == target.user_input_id).first()
        print(f"\nUser Input ID: {target.user_input_id}")
        print(f"Query: {user_input.user_query}")
        print(f"Target Protein: {target.target_protein}g")
        print(f"Target Carbs: {target.target_carbs}g")
        print(f"Created: {target.created_at}")
    
    db.close()

if __name__ == "__main__":
    main() 