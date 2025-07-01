import pytest
from unittest.mock import patch, MagicMock
from app.core.recommendation import (
    extract_soft_guidance,
    _apply_hard_filters,
    _find_optimal_snack_combination,
    get_recommendations
)
from app.schemas.recommendation import RecommendationRequest
from app.db.models import Product, MacroTarget, UserInput
from app.core.macro_targeting import MacroTargetingService

# 1. Test soft guidance extraction
def test_extract_soft_guidance():
    context = """
    Prioritize snacks with more protein than fiber.
    Favor fast-digesting carbs.
    Avoid high-fat foods.
    """
    result = extract_soft_guidance(context)
    assert "Prioritize" in result and "Favor" in result

# 2. Test hard filtering
def test_apply_hard_filters():
    products = [
        Product(name="A", dietary_flags=["vegan"], description="no peanuts"),
        Product(name="B", dietary_flags=["vegan"], description="contains peanuts"),
        Product(name="C", dietary_flags=["gluten-free"], description="no peanuts"),
    ]
    preferences = {"dietary_restrictions": ["vegan"], "ingredient_exclusions": ["peanuts"]}
    filtered = _apply_hard_filters(products, preferences)
    assert all("vegan" in p.dietary_flags for p in filtered)
    assert all("peanuts" not in p.description for p in filtered)

# 3. Test combination optimization
def test_find_optimal_snack_combination():
    products = [
        Product(name="A", protein=10, carbs=10, fat=5, calories=100),
        Product(name="B", protein=5, carbs=20, fat=5, calories=150),
        Product(name="C", protein=15, carbs=5, fat=10, calories=200),
        Product(name="D", protein=0, carbs=30, fat=0, calories=120),
        Product(name="E", protein=8, carbs=8, fat=8, calories=80),
    ]
    macro_target = MacroTarget(target_protein=20, target_carbs=30, target_fat=10, target_calories=250)
    combo = _find_optimal_snack_combination(products, macro_target, min_snacks=2, max_snacks=3)
    total_protein = sum(p.protein or 0 for p in combo)
    total_carbs = sum(p.carbs or 0 for p in combo)
    assert len(combo) >= 2
    assert abs(total_protein - 20) < 10  # within 10g
    assert abs(total_carbs - 30) < 10

# 4. Test end-to-end recommendation with all external calls mocked
@pytest.mark.asyncio
@patch("app.core.macro_targeting.MacroTargetingService.get_context_and_macro_targets")
@patch("app.core.recommendation._apply_hard_filters")
@patch("app.core.recommendation._find_optimal_snack_combination")
async def test_get_recommendations(
    mock_find_combo, mock_hard_filters, mock_get_context_and_targets
):
    # Mock macro target and context
    macro_target = MacroTarget(
        target_protein=20, target_carbs=30, target_fat=10, target_calories=250, target_electrolytes=1
    )
    mock_get_context_and_targets.return_value = (
        "Prioritize snacks with more protein than fiber.", macro_target
    )
    # Mock filtered products and combo
    products = [
        Product(name="A", protein=10, carbs=10, fat=5, calories=100),
        Product(name="B", protein=5, carbs=20, fat=5, calories=150),
    ]
    mock_hard_filters.return_value = products
    mock_find_combo.return_value = products

    # Create a fake DB session (can be a MagicMock)
    db = MagicMock()
    request = RecommendationRequest(
        user_query="test",
        preferences={"dietary_restrictions": ["vegan"]}
    )
    result = await get_recommendations(request, db)
    assert result.macro_targets.target_protein == 20
    assert len(result.recommended_products) == 2

def test_generate_macro_targets_parses_gpt_json():
    # Simulate a user input
    user_input = UserInput(
        id=1,
        user_query="What should I eat after soccer?",
        age=20,
        weight_kg=70,
        sex="male",
        exercise_type="soccer",
        exercise_duration_minutes=90,
        exercise_intensity="high",
        timing="post-workout"
    )

    # Simulate a GPT JSON response
    fake_gpt_response = MagicMock()
    fake_gpt_response.content = '''
    {
        "target_calories": 400,
        "target_protein": 30,
        "target_carbs": 60,
        "target_fat": 10,
        "target_electrolytes": 2.5
    }
    '''

    # Patch ChatOpenAI to return the fake response
    with patch("app.core.macro_targeting.ChatOpenAI") as MockLLM, \
         patch("app.core.macro_targeting.OpenAIEmbeddings"):
        mock_llm_instance = MockLLM.return_value
        mock_llm_instance.__call__.return_value = fake_gpt_response

        service = MacroTargetingService(openai_api_key="sk-fake")
        # Patch retrieve_context to avoid vectorstore call
        service.retrieve_context = MagicMock(return_value="context")

        macro_target = service.generate_macro_targets(user_input)

        assert macro_target.target_calories == 400
        assert macro_target.target_protein == 30
        assert macro_target.target_carbs == 60
        assert macro_target.target_fat == 10
        assert macro_target.target_electrolytes == 2.5 