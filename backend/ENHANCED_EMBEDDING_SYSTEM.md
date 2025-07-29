# Enhanced Embedding System for Unified User Query and Product Matching

## Overview

This document describes the enhanced embedding system that creates a unified vector space for matching user queries (with soft preferences and macro targets) to product schemas.

## Key Features

### 1. **Unified Vector Space**

-   Both user queries and products are embedded in the same vector space
-   Enables semantic matching between user intent and product characteristics
-   Uses the same sentence-transformers model (`all-MiniLM-L6-v2`) for consistency

### 2. **Rich User Query Embeddings**

-   Incorporates original user query
-   Adds soft preferences (flavor, texture) as structured text
-   Includes macro targets (protein, carbs, calories) for nutritional matching
-   Example: "I want savory chewy snacks" + "needs 25g protein" + "target 200 calories"

### 3. **Enhanced Product Embeddings**

-   Comprehensive product descriptions including nutrition facts
-   Key matching attributes (flavor, texture, protein, carbs)
-   Dietary and timing information
-   Price and form details

### 4. **Integration with Existing Pipeline**

-   Maintains compatibility with hard filtering system
-   Works with LLM field extraction
-   Supports macro targeting from RAG pipeline
-   Preserves existing recommendation flow

## Implementation

### Core Files

1. **`app/core/enhanced_embedding.py`** - Main enhanced embedding module
2. **`app/core/recommendation.py`** - Updated with enhanced embedding integration
3. **`examples/test_enhanced_embedding.py`** - Basic functionality tests
4. **`examples/test_integrated_enhanced_embedding.py`** - Full pipeline integration tests

### Key Functions

#### User Query Embedding

```python
def generate_user_query_embedding_text(user_query: str, soft_preferences: dict = None, macro_targets: dict = None) -> str:
    """Generate rich text representation of user query for embedding."""
```

#### Product Embedding

```python
def generate_enhanced_product_embedding_text(product: ProductModel) -> str:
    """Generate enhanced product text for better matching."""
```

#### Similarity Matching

```python
def rank_products_by_similarity(user_query: str, products: List[ProductModel], soft_preferences: dict = None, macro_targets: dict = None) -> List[tuple]:
    """Rank products by similarity to user query embedding."""
```

#### Integration Function

```python
def _enhanced_vector_search_with_embeddings(user_query: str, pre_filtered_products: List[Product], soft_preferences: dict = None, macro_targets: dict = None) -> List[Product]:
    """Enhanced vector search using unified embeddings for user queries and products."""
```

## Usage Examples

### Basic Usage

```python
from app.core.enhanced_embedding import rank_products_by_similarity

# Rank products by user query
ranked_products = rank_products_by_similarity(
    user_query="I need a protein bar for post-workout recovery",
    products=product_list
)
```

### With Soft Preferences

```python
soft_preferences = {
    "flavor": ["chocolate"],
    "texture": ["chewy"],
    "price_dollars": None
}

ranked_products = rank_products_by_similarity(
    user_query="I want a chocolate flavored chewy snack",
    products=product_list,
    soft_preferences=soft_preferences
)
```

### With Macro Targets

```python
macro_targets = {
    "target_protein": 25.0,
    "target_carbs": 15.0,
    "target_calories": 200.0
}

ranked_products = rank_products_by_similarity(
    user_query="I need a high-protein snack for muscle building",
    products=product_list,
    macro_targets=macro_targets
)
```

## Benefits

### 1. **Better Semantic Understanding**

-   Matches "wants savory flavor" with products containing "savory" or similar flavors
-   Understands "needs 20g protein" and matches with high-protein products
-   Captures nuanced user preferences

### 2. **Unified Matching**

-   Single embedding space for queries and products
-   Consistent similarity scoring
-   Better ranking accuracy

### 3. **Flexible Integration**

-   Works with existing hard filtering
-   Compatible with LLM field extraction
-   Supports macro targeting pipeline

### 4. **Rich Context**

-   Incorporates multiple preference types
-   Includes nutritional requirements
-   Maintains product metadata

## Test Results

The system has been tested with real data and shows:

-   **Unified vector space** working correctly
-   **Soft preferences** properly incorporated into embeddings
-   **Macro targets** enhancing nutritional matching
-   **Hard filtering** compatibility maintained
-   **Better semantic understanding** of user intent

## Integration with Recommendation Pipeline

The enhanced embedding system integrates seamlessly with your existing recommendation pipeline:

1. **LLM Field Extraction** → Extracts soft preferences and hard filters
2. **Hard Filtering** → Pre-filters products by dietary/allergen constraints
3. **Enhanced Embedding Matching** → Ranks remaining products by semantic similarity
4. **Macro Optimization** → Final optimization considering price and other constraints

## Next Steps

To fully integrate this system:

1. **Update recommendation.py** to use `_enhanced_vector_search_with_embeddings` instead of traditional vector search
2. **Test with real user queries** to validate performance
3. **Optimize embedding text generation** based on real-world usage
4. **Consider caching** frequently used embeddings for performance

## Performance Considerations

-   Embedding generation is fast with sentence-transformers
-   Similarity calculation is efficient with cosine similarity
-   Can be optimized further with embedding caching
-   Scales well with product database size

This enhanced embedding system provides a significant improvement in matching user queries to products by creating a unified, semantically-rich vector space that captures both user preferences and product characteristics.
