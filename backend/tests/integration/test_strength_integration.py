#!/usr/bin/env python3
"""
Integration test for strength activity detection in the full recommendation pipeline.

This test verifies that when a strength activity is detected, the high-protein
preference is added and used in the recommendation pipeline.
"""

import pytest
from unittest.mock import Mock, patch
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput, MacroTarget, Product
from app.schemas.recommendation import RecommendationRequest
from app.core.recommendation import get_recommendations
from sqlalchemy.orm import Session


class TestStrengthIntegration:
    """Integration tests for strength activity detection in recommendation pipeline."""
    
    @patch('app.core.macro_targeting_local.MacroTargetingServiceLocal._initialize_vectorstore')
    @patch('app.db.vector_store.get_product_vector_store')
    @patch('app.core.layer2_macro_optimization.optimize_macro_combination')
    def test_strength_activity_adds_high_protein_preference(self, mock_optimize, mock_vector_store, mock_init):
        """Test that strength activities add high-protein preference in full pipeline."""
        
        # Create a mock user input with strength activity
        request = RecommendationRequest(
            user_query="I need snacks for my weightlifting session",
            age=25,
            weight_kg=70,
            exercise_type="weightlifting",
            exercise_duration_minutes=60
        )
        
        # Mock the macro targeting service
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            # Mock the vector store get method to return strength metadata
            mock_metadata = {
                'type_of_activity': 'strength',
                'duration': 'long',
                'age_group': '19-59'
            }
            mock_results = {
                'documents': ['mock document content'],
                'metadatas': [mock_metadata]
            }
            service.vectorstore = Mock()
            service.vectorstore.get.return_value = mock_results
            
            # Mock the generate_macro_targets method
            mock_macro_target = Mock(spec=MacroTarget)
            mock_macro_target.target_protein = 25.0
            mock_macro_target.target_carbs = 30.0
            mock_macro_target.target_calories = 200.0
            service.generate_macro_targets = Mock(return_value=mock_macro_target)
            
            # Test that high-protein preference is added
            context, macro_target = service.get_context_and_macro_targets(
                UserInput(**request.model_dump())
            )
            
            # Verify that high-protein was added to soft preferences
            user_input = UserInput(**request.model_dump())
            context, macro_target = service.get_context_and_macro_targets(user_input)
            
            assert user_input.preferences is not None
            assert 'soft_preferences' in user_input.preferences
            assert 'dietary' in user_input.preferences['soft_preferences']
            assert 'high-protein' in user_input.preferences['soft_preferences']['dietary']
            
            print("High-protein preference was successfully added for strength activity")
    
    @patch('app.core.macro_targeting_local.MacroTargetingServiceLocal._initialize_vectorstore')
    def test_strength_detection_from_exercise_keywords(self, mock_init):
        """Test that strength activities are detected from exercise type keywords."""
        
        # Test various strength-related exercise types
        strength_exercises = [
            "weightlifting",
            "gym workout", 
            "resistance training",
            "plyometrics",
            "strength training"
        ]
        
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            for exercise_type in strength_exercises:
                user_input = UserInput(
                    user_query=f"I need snacks for my {exercise_type}",
                    age=25,
                    weight_kg=70,
                    exercise_type=exercise_type,
                    exercise_duration_minutes=60
                )
                
                strength_detected = service._detect_strength_in_retrieved_metadata(None, user_input)
                assert strength_detected == True, f"Failed to detect strength for: {exercise_type}"
                print(f"Detected strength activity for: {exercise_type}")
    
    @patch('app.core.macro_targeting_local.MacroTargetingServiceLocal._initialize_vectorstore')
    def test_cardio_activities_dont_add_high_protein(self, mock_init):
        """Test that cardio activities do NOT add high-protein preference."""
        
        # Test various cardio exercise types
        cardio_exercises = [
            "running",
            "cycling", 
            "swimming",
            "soccer",
            "basketball"
        ]
        
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            # Mock the vector store get method to return cardio metadata
            mock_metadata = {
                'type_of_activity': 'cardio',
                'duration': 'long',
                'age_group': '19-59'
            }
            mock_results = {
                'documents': ['mock document content'],
                'metadatas': [mock_metadata]
            }
            service.vectorstore = Mock()
            service.vectorstore.get.return_value = mock_results
            
            for exercise_type in cardio_exercises:
                user_input = UserInput(
                    user_query=f"I need snacks for my {exercise_type}",
                    age=25,
                    weight_kg=70,
                    exercise_type=exercise_type,
                    exercise_duration_minutes=60
                )
                
                # Mock the generate_macro_targets method
                mock_macro_target = Mock(spec=MacroTarget)
                service.generate_macro_targets = Mock(return_value=mock_macro_target)
                
                context, macro_target = service.get_context_and_macro_targets(user_input)
                
                # Verify that high-protein was NOT added
                if hasattr(user_input, 'preferences') and user_input.preferences:
                    if 'soft_preferences' in user_input.preferences:
                        if 'dietary' in user_input.preferences['soft_preferences']:
                            assert 'high-protein' not in user_input.preferences['soft_preferences']['dietary'], f"High-protein incorrectly added for: {exercise_type}"
                
                print(f"No high-protein preference added for cardio: {exercise_type}")


if __name__ == "__main__":
    # Run the tests
    test = TestStrengthIntegration()
    test.test_strength_activity_adds_high_protein_preference()
    test.test_strength_detection_from_exercise_keywords()
    test.test_cardio_activities_dont_add_high_protein()
    print("\nAll strength detection integration tests passed!") 