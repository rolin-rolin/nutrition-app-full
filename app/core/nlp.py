from typing import Dict
import re

def normalize_text(text: str) -> str:
    """
    Lowercase, remove extra whitespace, and basic cleaning.
    """
    return re.sub(r'\s+', ' ', text.strip().lower())

def parse_user_query(query: str) -> Dict:
    """
    Parse user query into structured information (e.g., extract goals, preferences).
    Placeholder for more advanced NLP logic.
    """
    # Example: return {"goals": ..., "preferences": ...}
    return {"raw_query": query}

def construct_prompt(user_query: str, examples: list = None) -> str:
    """
    Construct a prompt for GenAI, optionally with few-shot examples.
    """
    prompt = "You are a nutrition expert. Based on the following user query, recommend suitable products.\n"
    if examples:
        for ex in examples:
            prompt += f"Example: {ex}\n"
    prompt += f"User Query: {user_query}\nRecommendations:"
    return prompt 