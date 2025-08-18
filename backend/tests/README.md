# Test Organization

This directory contains all tests for the nutrition app, organized by category and purpose.

## Directory Structure

```
tests/
├── README.md                 # This file - test documentation
├── conftest.py              # Pytest configuration and shared fixtures
├── unit/                    # Unit tests for individual functions/classes
│   └── test_recommendation_unit.py
├── integration/             # Integration tests for component interactions
│   ├── test_json_output.py
│   └── test_recommendation.py
├── rag/                     # RAG pipeline specific tests
│   └── test_rag_pipeline.py
└── utils/                   # Utility scripts and helper tests
    ├── test_document_loading.py
    └── rebuild_vectorstore.py
```

## Test Categories

### 1. Unit Tests (`unit/`)

**Purpose**: Test individual functions and classes in isolation
**Characteristics**:

-   Mock external dependencies (APIs, databases)
-   Fast execution
-   Focus on specific functionality
-   High code coverage

**Files**:

-   `test_recommendation_unit.py`: Tests for recommendation engine functions
    -   `extract_soft_guidance()`
    -   `_apply_hard_filters()`
    -   `_find_optimal_snack_combination()`
    -   `get_recommendations()` (mocked)
    -   `extract_user_input_fields_llm()`

### 2. Integration Tests (`integration/`)

**Purpose**: Test interactions between components
**Characteristics**:

-   May use real external services (with API keys)
-   Test component boundaries
-   Slower than unit tests
-   Verify end-to-end workflows

**Files**:

-   `test_json_output.py`: Tests GPT JSON response parsing
    -   Tests actual OpenAI API integration
    -   Validates JSON structure and parsing
    -   Requires `OPENAI_API_KEY` environment variable
-   `test_recommendation.py`: Tests full recommendation pipeline
    -   Tests end-to-end flow from user input to snack recommendations
    -   Validates macro target generation and product matching
    -   Tests multiple user scenarios with different preferences

### 3. RAG Pipeline Tests (`rag/`)

**Purpose**: Test the RAG (Retrieval-Augmented Generation) pipeline
**Characteristics**:

-   Test document loading and vector store operations
-   Verify context retrieval accuracy
-   Test query building and matching

**Files**:

-   `test_rag_pipeline.py`: Tests complete RAG workflow
    -   Document loading from nutrition guidelines
    -   Query building with age/exercise classification
    -   Context retrieval (requires API quota)

### 4. Utility Tests (`utils/`)

**Purpose**: Helper scripts and maintenance tools
**Characteristics**:

-   Not traditional tests, but utility scripts
-   Used for setup, maintenance, and debugging
-   Can be run independently

**Files**:

-   `test_document_loading.py`: Verify nutrition guideline document loading
    -   Tests document parsing without API calls
    -   Validates metadata assignment
    -   Shows document statistics
-   `rebuild_vectorstore.py`: Rebuild the Chroma vector store
    -   Clears existing vector store
    -   Reloads all nutrition guideline documents
    -   Useful for updates to guidelines
