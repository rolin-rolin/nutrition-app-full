#!/usr/bin/env python3
"""
Test strength activity detection and high-protein preference addition.

This test verifies that when a strength activity is detected in the knowledge document
metadata, the system automatically adds "high-protein" as a soft preference for use
in the recommendation pipeline.
"""

import pytest
from unittest.mock import Mock, patch
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput, MacroTarget
from app.schemas.recommendation import RecommendationRequest
from app.core.recommendation import get_recommendations
from sqlalchemy.orm import Session


class TestStrengthHighProteinDetection:
    """Test cases for strength activity detection and high-protein preference addition."""
    
    def test_strength_detection_in_metadata(self):
        """Test that strength activities are detected from document metadata."""
        # Create a mock user input with strength activity
        user_input = UserInput(
            user_query="I need snacks for my weightlifting session",
            age=25,
            weight_kg=70,
            exercise_type="weightlifting",
            exercise_duration_minutes=60
        )
        
        # Create mock vector store results with strength metadata
        mock_metadata = {
            'type_of_activity': 'strength',
            'duration': 'long',
            'age_group': '19-59'
        }
        
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            # Mock the vector store get method to return strength metadata
            mock_results = {
                'documents': ['mock document content'],
                'metadatas': [mock_metadata]
            }
            service.vectorstore = Mock()
            service.vectorstore.get.return_value = mock_results
            
            # Test strength detection
            strength_detected = service._detect_strength_in_retrieved_metadata(mock_metadata, user_input)
            assert strength_detected == True
    
    def test_strength_detection_from_exercise_type(self):
        """Test that strength activities are detected from exercise type keywords."""
        # Create a mock user input with strength-related exercise type
        user_input = UserInput(
            user_query="I need snacks for my gym workout",
            age=25,
            weight_kg=70,
            exercise_type="gym workout",
            exercise_duration_minutes=60
        )
        
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            # Test strength detection from exercise type (no metadata available)
            strength_detected = service._detect_strength_in_retrieved_metadata(None, user_input)
            assert strength_detected == True
    
    def test_high_protein_preference_addition(self):
        """Test that high-protein preference is added when strength is detected."""
        # Create a mock user input with strength activity
        user_input = UserInput(
            user_query="I need snacks for my weightlifting session",
            age=25,
            weight_kg=70,
            exercise_type="weightlifting",
            exercise_duration_minutes=60
        )
        
        # Mock vector store results with strength metadata
        mock_metadata = {
            'type_of_activity': 'strength',
            'duration': 'long',
            'age_group': '19-59'
        }
        
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            # Mock the vector store get method
            mock_results = {
                'documents': ['mock document content'],
                'metadatas': [mock_metadata]
            }
            service.vectorstore = Mock()
            service.vectorstore.get.return_value = mock_results
            
            # Mock the generate_macro_targets method
            mock_macro_target = Mock(spec=MacroTarget)
            service.generate_macro_targets = Mock(return_value=mock_macro_target)
            
            # Test that high-protein preference is added
            context, macro_target = service.get_context_and_macro_targets(user_input)
            
            # Verify that high-protein was added to soft preferences
            assert user_input.preferences is not None
            assert 'soft_preferences' in user_input.preferences
            assert 'dietary' in user_input.preferences['soft_preferences']
            assert 'high-protein' in user_input.preferences['soft_preferences']['dietary']
    
    def test_no_strength_detection_for_cardio(self):
        """Test that high-protein preference is NOT added for cardio activities."""
        # Create a mock user input with cardio activity
        user_input = UserInput(
            user_query="I need snacks for my running session",
            age=25,
            weight_kg=70,
            exercise_type="running",
            exercise_duration_minutes=60
        )
        
        # Mock vector store results with cardio metadata
        mock_metadata = {
            'type_of_activity': 'cardio',
            'duration': 'long',
            'age_group': '19-59'
        }
        
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            # Mock the vector store get method
            mock_results = {
                'documents': ['mock document content'],
                'metadatas': [mock_metadata]
            }
            service.vectorstore = Mock()
            service.vectorstore.get.return_value = mock_results
            
            # Mock the generate_macro_targets method
            mock_macro_target = Mock(spec=MacroTarget)
            service.generate_macro_targets = Mock(return_value=mock_macro_target)
            
            # Test that high-protein preference is NOT added
            context, macro_target = service.get_context_and_macro_targets(user_input)
            
            # Verify that high-protein was NOT added to soft preferences
            if hasattr(user_input, 'preferences') and user_input.preferences:
                if 'soft_preferences' in user_input.preferences:
                    if 'dietary' in user_input.preferences['soft_preferences']:
                        assert 'high-protein' not in user_input.preferences['soft_preferences']['dietary']
    
    def test_existing_preferences_preserved(self):
        """Test that existing preferences are preserved when adding high-protein."""
        # Create a mock user input with existing preferences
        user_input = UserInput(
            user_query="I need snacks for my weightlifting session",
            age=25,
            weight_kg=70,
            exercise_type="weightlifting",
            exercise_duration_minutes=60,
            preferences={
                'soft_preferences': {
                    'flavor': ['savory'],
                    'texture': ['chewy'],
                    'dietary': ['gluten-free']
                }
            }
        )
        
        # Mock vector store results with strength metadata
        mock_metadata = {
            'type_of_activity': 'strength',
            'duration': 'long',
            'age_group': '19-59'
        }
        
        with patch.object(MacroTargetingServiceLocal, '_initialize_vectorstore'):
            service = MacroTargetingServiceLocal()
            
            # Mock the vector store get method
            mock_results = {
                'documents': ['mock document content'],
                'metadatas': [mock_metadata]
            }
            service.vectorstore = Mock()
            service.vectorstore.get.return_value = mock_results
            
            # Mock the generate_macro_targets method
            mock_macro_target = Mock(spec=MacroTarget)
            service.generate_macro_targets = Mock(return_value=mock_macro_target)
            
            # Test that existing preferences are preserved
            context, macro_target = service.get_context_and_macro_targets(user_input)
            
            # Verify that existing preferences are preserved
            assert user_input.preferences['soft_preferences']['flavor'] == ['savory']
            assert user_input.preferences['soft_preferences']['texture'] == ['chewy']
            assert user_input.preferences['soft_preferences']['dietary'] == ['gluten-free', 'high-protein']


if __name__ == "__main__":
    pytest.main([__file__]) 