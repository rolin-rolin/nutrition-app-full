import pytest
from app.core.recommendation import get_recommendations
from app.schemas.recommendation import RecommendationRequest, EnhancedRecommendationResponse
from app.db.session import get_db
from app.db.models import Product
from sqlalchemy.orm import Session


class TestEnhancedRecommendationResponse:
    """Test the enhanced recommendation response structure."""
    
    async def test_enhanced_response_structure(self, db: Session):
        """Test that the enhanced response includes all required fields."""
        # Create a test request with activity info
        request = RecommendationRequest(
            user_query="I need snacks for my workout",
            age=25,
            weight_kg=70.0,
            exercise_type="cardio",
            exercise_duration_minutes=60,
            preferences={
                "flavor_preferences": ["sweet"],
                "dietary_requirements": ["vegan"]
            }
        )
        
        # Get recommendations
        response = await get_recommendations(request, db)
        
        # Verify it's an enhanced response
        assert isinstance(response, EnhancedRecommendationResponse)
        
        # Verify user profile info
        assert response.user_profile is not None
        assert response.user_profile.age == 25
        assert response.user_profile.weight_kg == 70.0
        assert response.user_profile.exercise_type == "cardio"
        assert response.user_profile.exercise_duration_minutes == 60
        assert "25 years old" in response.user_profile.age_display
        assert "70kg" in response.user_profile.weight_display
        assert "cardio for 60 minutes" in response.user_profile.exercise_display
        
        # Verify macro targets
        assert response.macro_targets is not None
        assert response.macro_targets.target_protein is not None
        assert response.macro_targets.target_carbs is not None
        assert response.macro_targets.target_fat is not None
        assert response.macro_targets.target_calories is not None
        
        # Verify bundle stats (if optimization was successful)
        if response.bundle_stats:
            assert response.bundle_stats.total_protein >= 0
            assert response.bundle_stats.total_carbs >= 0
            assert response.bundle_stats.total_fat >= 0
            assert response.bundle_stats.total_calories >= 0
            assert response.bundle_stats.num_snacks > 0
            assert response.bundle_stats.target_match_percentage >= 0
        
        # Verify preferences
        assert response.preferences is not None
        assert "sweet flavor" in response.preferences.soft_preferences
        assert "vegan" in response.preferences.hard_filters
        
        # Verify key principles
        assert isinstance(response.key_principles, list)
        assert len(response.key_principles) <= 2  # Should be 0-2 principles
        
        # Verify products
        assert len(response.recommended_products) > 0
        for product in response.recommended_products:
            assert product.name is not None
            assert product.protein is not None
            assert product.carbs is not None
            assert product.fat is not None
            assert product.calories is not None
    
    async def test_enhanced_response_with_defaults(self, db: Session):
        """Test enhanced response when using default values."""
        # Create a minimal request
        request = RecommendationRequest(
            user_query="I need snacks",
            preferences={
                "flavor_preferences": ["sweet"]
            }
        )
        
        # Get recommendations
        response = await get_recommendations(request, db)
        
        # Verify it's an enhanced response
        assert isinstance(response, EnhancedRecommendationResponse)
        
        # User profile should be None when no activity info
        assert response.user_profile is None
        
        # Macro targets should be None when no activity info
        assert response.macro_targets is None
        
        # Bundle stats should be None when no activity info
        assert response.bundle_stats is None
        
        # Preferences should still be populated
        assert response.preferences is not None
        assert "sweet flavor" in response.preferences.soft_preferences
        
        # Key principles should be empty when no activity info
        assert len(response.key_principles) == 0
        
        # Products should still be returned
        assert len(response.recommended_products) > 0
    
    async def test_enhanced_response_with_strength_activity(self, db: Session):
        """Test enhanced response with strength activity detection."""
        request = RecommendationRequest(
            user_query="I need snacks for weightlifting",
            age=30,
            weight_kg=80.0,
            exercise_type="weightlifting",
            exercise_duration_minutes=90,
            preferences={
                "flavor_preferences": ["sweet"]
            }
        )
        
        # Get recommendations
        response = await get_recommendations(request, db)
        
        # Verify it's an enhanced response
        assert isinstance(response, EnhancedRecommendationResponse)
        
        # User profile should include strength activity
        assert response.user_profile is not None
        assert "weightlifting" in response.user_profile.exercise_display
        
        # Preferences should include high-protein from strength detection
        assert response.preferences is not None
        assert "high-protein" in response.preferences.soft_preferences
        
        # Key principles should be extracted from strength document
        assert len(response.key_principles) <= 2
        
        # Products should be returned
        assert len(response.recommended_products) > 0 