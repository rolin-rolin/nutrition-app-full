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

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run by Category

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# RAG tests only
pytest tests/rag/
```

### Run Utility Scripts

```bash
# Test document loading
python tests/utils/test_document_loading.py

# Rebuild vector store
python tests/utils/rebuild_vectorstore.py
```

### Run Specific Test Files

```bash
# Run specific test file
pytest tests/unit/test_recommendation_unit.py

# Run with verbose output
pytest tests/unit/test_recommendation_unit.py -v

# Run specific test function
pytest tests/unit/test_recommendation_unit.py::test_extract_soft_guidance
```

## Test Dependencies

### Environment Variables

-   `OPENAI_API_KEY`: Required for integration tests and RAG tests
-   `DATABASE_URL`: For database integration tests

### External Services

-   OpenAI API: For GPT integration tests
-   Chroma Vector Store: For RAG pipeline tests
-   SQLite Database: For database tests

## Test Data

### Sample Products

Tests use sample product data defined in `init_db.py`:

-   Protein bars, nuts, yogurt, fruits, etc.
-   Various nutritional profiles
-   Different dietary flags and categories

### Nutrition Guidelines

RAG tests use the structured nutrition guidelines:

-   Age-specific recommendations (6-11, 12-18, 19-59)
-   Exercise type specific (cardio, strength)
-   Duration specific (short, long sessions)

## Best Practices

1. **Mock External APIs**: Use mocks for unit tests to avoid API costs
2. **Test Data Isolation**: Each test should use isolated test data
3. **Clear Test Names**: Use descriptive test function names
4. **Documentation**: Add docstrings to complex test functions
5. **Error Handling**: Test both success and failure scenarios

## Adding New Tests

### Unit Tests

1. Create test file in `tests/unit/`
2. Use descriptive filename: `test_<module_name>_unit.py`
3. Mock external dependencies
4. Test individual functions/classes

### Integration Tests

1. Create test file in `tests/integration/`
2. Test component interactions
3. May require real API keys
4. Document external dependencies

### RAG Tests

1. Create test file in `tests/rag/`
2. Test document loading and retrieval
3. Verify query matching accuracy
4. Test age/exercise classification

### Utility Scripts

1. Create script in `tests/utils/`
2. Add clear documentation
3. Make scripts runnable independently
4. Include usage examples
