#!/usr/bin/env python3
"""
Test YAML-based macro calculation functionality.
"""

import pytest
import yaml
from unittest.mock import Mock
from app.core.macro_targeting_local import MacroTargetingServiceLocal
from app.db.models import UserInput


class TestYAMLMacroCalculation:
    """Test the YAML-based macro calculation functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = MacroTargetingServiceLocal()
        
        # Sample YAML content from the nutrition guidelines
        self.sample_yaml_content = """
---
type_of_activity: cardio
duration: long
age_group: 6-11
---

timing:
pre:
carbs_g_per_kg: [0.5, 0.8]
protein_g_per_kg: [0.05, 0.1]
fat_g_per_kg: [0.1, 0.1]

during:
carbs_g_per_kg_per_hour: [0.5, 1.0]
electrolytes_mg_per_kg_per_hour: [11, 21]

post:
carbs_g_per_kg: [1.0, 1.0]
protein_g_per_kg: [0.2, 0.25]
fat_g_per_kg: [0.1, 0.2]
"""
    
    def test_calculate_range_single_value(self):
        """Test _calculate_range with a single value."""
        result = self.service._calculate_range([0.5], 40.0)
        assert result == 20.0  # 0.5 * 40
    
    def test_calculate_range_multiple_values(self):
        """Test _calculate_range with multiple values (range)."""
        result = self.service._calculate_range([0.5, 0.8], 40.0)
        expected = ((0.5 + 0.8) / 2) * 40.0  # Average of range * weight
        assert result == expected
    
    def test_calculate_range_empty_list(self):
        """Test _calculate_range with empty list."""
        result = self.service._calculate_range([], 40.0)
        assert result == 0.0
    
    def test_extract_macro_values_from_yaml(self):
        """Test extracting macro values from YAML content."""
        # Create a mock user input
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=10,
            weight_kg=40.0,  # Used for accurate calculations when provided, defaults to 70kg if missing
            sex="male",
            exercise_type="soccer",
            exercise_duration_minutes=90,  # 1.5 hours
            exercise_intensity="high",
            timing="post-workout"
        )
        
        # Calculate macros from YAML
        macro_values = self.service._extract_macro_values_from_context(self.sample_yaml_content, user_input)
        
        # Verify the structure
        assert 'target_calories' in macro_values
        assert 'target_protein' in macro_values
        assert 'target_carbs' in macro_values
        assert 'target_fat' in macro_values
        assert 'target_electrolytes' in macro_values
        assert 'pre_workout_macros' in macro_values
        assert 'during_workout_macros' in macro_values
        assert 'post_workout_macros' in macro_values
        
        # Verify calculations for a 40kg child doing 90 minutes of cardio
        # Pre-workout: carbs = avg(0.5, 0.8) * 40 = 26g, protein = avg(0.05, 0.1) * 40 = 3g
        expected_pre_carbs = ((0.5 + 0.8) / 2) * 40.0
        expected_pre_protein = ((0.05 + 0.1) / 2) * 40.0
        
        # During: carbs = avg(0.5, 1.0) * 40 * 1.5 = 45g, electrolytes = avg(11, 21) * 40 * 1.5 = 480mg
        # During: protein = avg(0, 0) * 40 * 1.5 = 0g, fat = avg(0, 0) * 40 * 1.5 = 0g (from sample YAML)
        expected_during_carbs = ((0.5 + 1.0) / 2) * 40.0 * 1.5
        expected_during_protein = 0.0  # No protein in sample YAML during section
        expected_during_fat = 0.0      # No fat in sample YAML during section
        expected_during_electrolytes = ((11 + 21) / 2) * 40.0 * 1.5
        
        # Post: carbs = 1.0 * 40 = 40g, protein = avg(0.2, 0.25) * 40 = 9g
        expected_post_carbs = 1.0 * 40.0
        expected_post_protein = ((0.2 + 0.25) / 2) * 40.0
        
        # Verify pre-workout values
        assert abs(macro_values['pre_workout_macros']['carbs'] - expected_pre_carbs) < 0.1
        assert abs(macro_values['pre_workout_macros']['protein'] - expected_pre_protein) < 0.1
        
        # Verify during-workout values
        assert abs(macro_values['during_workout_macros']['carbs'] - expected_during_carbs) < 0.1
        assert abs(macro_values['during_workout_macros']['protein'] - expected_during_protein) < 0.1
        assert abs(macro_values['during_workout_macros']['fat'] - expected_during_fat) < 0.1
        assert abs(macro_values['during_workout_macros']['electrolytes'] - expected_during_electrolytes) < 0.1
        
        # Verify post-workout values
        assert abs(macro_values['post_workout_macros']['carbs'] - expected_post_carbs) < 0.1
        assert abs(macro_values['post_workout_macros']['protein'] - expected_post_protein) < 0.1
        
        # Verify totals (now including during-workout protein and fat)
        total_carbs = expected_pre_carbs + expected_during_carbs + expected_post_carbs
        total_protein = expected_pre_protein + expected_during_protein + expected_post_protein
        total_electrolytes = expected_during_electrolytes
        
        assert abs(macro_values['target_carbs'] - total_carbs) < 0.1
        assert abs(macro_values['target_protein'] - total_protein) < 0.1
        assert abs(macro_values['target_electrolytes'] - total_electrolytes) < 0.1
    
    def test_extract_macro_values_with_defaults(self):
        """Test extracting macro values when weight is missing (should use default gracefully)."""
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=10,
            weight_kg=None,  # Missing weight - should use default
            exercise_type="soccer",
            exercise_duration_minutes=90
        )
        
        # Calculate macros from YAML
        macro_values = self.service._extract_macro_values_from_context(self.sample_yaml_content, user_input)
        
        # Should still return valid macro values using default weight (70kg)
        assert 'target_calories' in macro_values
        assert 'target_protein' in macro_values
        assert 'target_carbs' in macro_values
        assert 'target_fat' in macro_values
        assert 'target_electrolytes' in macro_values
        
        # Values should be calculated using default weight of 70kg
        # Pre-workout carbs = avg(0.5, 0.8) * 70 = 45.5g
        expected_pre_carbs = ((0.5 + 0.8) / 2) * 70.0
        assert abs(macro_values['pre_workout_macros']['carbs'] - expected_pre_carbs) < 0.1
    
    def test_fallback_to_default_values(self):
        """Test fallback to default values when YAML parsing fails."""
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=25,
            weight_kg=70.0,
            exercise_type="running",
            exercise_duration_minutes=60
        )
        
        # Use invalid YAML content
        invalid_content = "This is not valid YAML content"
        
        macro_values = self.service._extract_macro_values_from_context(invalid_content, user_input)
        
        # Should fall back to default values
        assert 'target_calories' in macro_values
        assert 'target_protein' in macro_values
        assert 'target_carbs' in macro_values
        assert 'target_fat' in macro_values
        assert 'target_electrolytes' in macro_values
    
    def test_generate_macro_targets_with_yaml(self):
        """Test the complete generate_macro_targets method with YAML content."""
        # Mock the retrieve_context_by_metadata method
        self.service.retrieve_context_by_metadata = Mock(return_value=self.sample_yaml_content)
        
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=10,
            weight_kg=40.0,
            exercise_type="soccer",
            exercise_duration_minutes=90
        )
        
        macro_target = self.service.generate_macro_targets(user_input)
        
        # Verify the macro target object
        assert macro_target.user_input_id == 1
        assert macro_target.target_calories is not None
        assert macro_target.target_protein is not None
        assert macro_target.target_carbs is not None
        assert macro_target.target_fat is not None
        assert macro_target.target_electrolytes is not None
        assert macro_target.pre_workout_macros is not None
        assert macro_target.during_workout_macros is not None
        assert macro_target.post_workout_macros is not None
        assert macro_target.rag_context == self.sample_yaml_content
        assert "YAML-based calculations" in macro_target.reasoning 

    def test_generate_macro_targets_with_missing_info(self):
        """Test the complete generate_macro_targets method with missing user information."""
        # Mock the retrieve_context_by_metadata method
        self.service.retrieve_context_by_metadata = Mock(return_value=self.sample_yaml_content)
        
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=25,
            weight_kg=None,  # Missing weight
            exercise_type="running",
            exercise_duration_minutes=None  # Missing duration
        )
        
        macro_target = self.service.generate_macro_targets(user_input)
        
        # Verify the macro target object
        assert macro_target.user_input_id == 1
        assert macro_target.target_calories is not None
        assert macro_target.target_protein is not None
        assert macro_target.target_carbs is not None
        assert macro_target.target_fat is not None
        assert macro_target.target_electrolytes is not None
        assert macro_target.pre_workout_macros is not None
        assert macro_target.during_workout_macros is not None
        assert macro_target.post_workout_macros is not None
        assert macro_target.rag_context == self.sample_yaml_content
        
        # Verify reasoning indicates defaults were used
        reasoning = macro_target.reasoning
        assert "using default 70kg weight" in reasoning
        assert "using default 60-minute duration" in reasoning
        assert "YAML-based calculations" in reasoning
    
    def test_generate_macro_targets_with_all_defaults(self):
        """Test the complete generate_macro_targets method with all fields missing (should use all defaults)."""
        # Mock the retrieve_context_by_metadata method
        self.service.retrieve_context_by_metadata = Mock(return_value=self.sample_yaml_content)
        
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=None,  # Missing age
            weight_kg=None,  # Missing weight
            exercise_type=None,  # Missing exercise type
            exercise_duration_minutes=None  # Missing duration
        )
        
        macro_target = self.service.generate_macro_targets(user_input)
        
        # Verify the macro target object
        assert macro_target.user_input_id == 1
        assert macro_target.target_calories is not None
        assert macro_target.target_protein is not None
        assert macro_target.target_carbs is not None
        assert macro_target.target_fat is not None
        assert macro_target.target_electrolytes is not None
        assert macro_target.pre_workout_macros is not None
        assert macro_target.during_workout_macros is not None
        assert macro_target.post_workout_macros is not None
        assert macro_target.rag_context == self.sample_yaml_content
        
        # Verify reasoning indicates all defaults were used
        reasoning = macro_target.reasoning
        assert "using default values (age: 21, weight: 70kg)" in reasoning
        assert "doing cardio (using default 60-minute duration)" in reasoning
        assert "YAML-based calculations" in reasoning 

    def test_extract_macro_values_with_during_protein_fat(self):
        """Test extracting macro values when YAML includes during-workout protein and fat."""
        # Create YAML content that includes during-workout protein and fat
        yaml_with_during_protein_fat = """
---
type_of_activity: strength
duration: long
age_group: 19-59
---

timing:
pre:
carbs_g_per_kg: [0.5, 0.8]
protein_g_per_kg: [0.1, 0.15]
fat_g_per_kg: [0.1, 0.15]

during:
carbs_g_per_kg_per_hour: [0.3, 0.5]
protein_g_per_kg_per_hour: [0.05, 0.1]
fat_g_per_kg_per_hour: [0.02, 0.05]
electrolytes_mg_per_kg_per_hour: [8, 15]

post:
carbs_g_per_kg: [1.2, 1.5]
protein_g_per_kg: [0.3, 0.4]
fat_g_per_kg: [0.1, 0.2]
"""
        
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=25,
            weight_kg=70.0,
            exercise_type="strength",
            exercise_duration_minutes=90  # 1.5 hours
        )
        
        # Calculate macros from YAML
        macro_values = self.service._extract_macro_values_from_context(yaml_with_during_protein_fat, user_input)
        
        # Verify during-workout protein and fat are calculated
        during_protein = macro_values['during_workout_macros']['protein']
        during_fat = macro_values['during_workout_macros']['fat']
        
        # Expected: avg(0.05, 0.1) * 70 * 1.5 = 3.9375g protein
        # Expected: avg(0.02, 0.05) * 70 * 1.5 = 1.8375g fat
        expected_during_protein = ((0.05 + 0.1) / 2) * 70.0 * 1.5
        expected_during_fat = ((0.02 + 0.05) / 2) * 70.0 * 1.5
        
        assert abs(during_protein - expected_during_protein) < 0.1
        assert abs(during_fat - expected_during_fat) < 0.1
        
        # Verify during-workout calories include protein and fat
        during_calories = macro_values['during_workout_macros']['calories']
        during_carbs = macro_values['during_workout_macros']['carbs']
        expected_during_calories = (during_carbs * 4) + (during_protein * 4) + (during_fat * 9)
        assert abs(during_calories - expected_during_calories) < 0.1
        
        # Verify totals include during-workout protein and fat
        total_protein = macro_values['target_protein']
        total_fat = macro_values['target_fat']
        assert total_protein > 0
        assert total_fat > 0
    
    def test_calorie_calculations_accuracy(self):
        """Test that calorie calculations are accurate and consistent."""
        # Create a simple YAML with known values
        simple_yaml = """
---
type_of_activity: cardio
duration: short
age_group: 19-59
---

timing:
pre:
carbs_g_per_kg: [1.0, 1.0]
protein_g_per_kg: [0.1, 0.1]
fat_g_per_kg: [0.05, 0.05]

during:
carbs_g_per_kg_per_hour: [0.5, 0.5]
protein_g_per_kg_per_hour: [0.02, 0.02]
fat_g_per_kg_per_hour: [0.01, 0.01]
electrolytes_mg_per_kg_per_hour: [10, 10]

post:
carbs_g_per_kg: [1.5, 1.5]
protein_g_per_kg: [0.2, 0.2]
fat_g_per_kg: [0.1, 0.1]
"""
        
        user_input = UserInput(
            id=1,
            user_query="Test query",
            age=25,
            weight_kg=60.0,  # Simple weight for easy calculations
            exercise_type="running",
            exercise_duration_minutes=60  # 1 hour
        )
        
        # Calculate macros from YAML
        macro_values = self.service._extract_macro_values_from_context(simple_yaml, user_input)
        
        # Expected calculations for 60kg person, 1 hour:
        # Pre: carbs=60g, protein=6g, fat=3g
        # During: carbs=30g, protein=1.2g, fat=0.6g  
        # Post: carbs=90g, protein=12g, fat=6g
        
        # Verify individual timing calories
        pre_calories = macro_values['pre_workout_macros']['calories']
        during_calories = macro_values['during_workout_macros']['calories']
        post_calories = macro_values['post_workout_macros']['calories']
        
        expected_pre_calories = (60 * 4) + (6 * 4) + (3 * 9)  # 240 + 24 + 27 = 291
        expected_during_calories = (30 * 4) + (1.2 * 4) + (0.6 * 9)  # 120 + 4.8 + 5.4 = 130.2
        expected_post_calories = (90 * 4) + (12 * 4) + (6 * 9)  # 360 + 48 + 54 = 462
        
        assert abs(pre_calories - expected_pre_calories) < 0.1
        assert abs(during_calories - expected_during_calories) < 0.1
        assert abs(post_calories - expected_post_calories) < 0.1
        
        # Verify total calories
        total_calories = macro_values['target_calories']
        expected_total = expected_pre_calories + expected_during_calories + expected_post_calories
        assert abs(total_calories - expected_total) < 0.1
        
        # Verify that total calories equals sum of timing calories
        calculated_total = pre_calories + during_calories + post_calories
        assert abs(total_calories - calculated_total) < 0.1 