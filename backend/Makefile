# Makefile for Nutrition App Tests
# Provides easy shortcuts for running different test categories

.PHONY: help test test-unit test-integration test-rag test-utils test-all clean docs

# Default target
help:
	@echo "Available commands:"
	@echo "  test-unit        - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-rag         - Run RAG pipeline tests only"
	@echo "  test-utils       - Run utility scripts"
	@echo "  test-all         - Run all test categories"
	@echo "  test             - Run all tests (alias for test-all)"
	@echo "  clean            - Clean up test artifacts"
	@echo "  docs             - Generate test documentation"

# Run all tests
test: test-all

# Run unit tests
test-unit:
	@echo "Running unit tests..."
	python -m pytest tests/unit/ -v

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	python -m pytest tests/integration/ -v

# Run RAG tests
test-rag:
	@echo "Running RAG pipeline tests..."
	python -m pytest tests/rag/ -v

# Run utility scripts
test-utils:
	@echo "Running utility scripts..."
	python tests/utils/test_document_loading.py
	python tests/utils/rebuild_vectorstore.py

# Run all test categories
test-all:
	@echo "Running all test categories..."
	python tests/run_tests.py all

# Clean up test artifacts
clean:
	@echo "Cleaning up test artifacts..."
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	rm -rf tests/__pycache__/
	rm -rf tests/*/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Generate test documentation
docs:
	@echo "Generating test documentation..."
	@echo "Test documentation is available in tests/README.md"

# Quick test (unit tests only, fast)
quick-test:
	@echo "Running quick test (unit tests only)..."
	python -m pytest tests/unit/ -v --tb=short

# Full test with coverage
test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# Test specific module
test-module:
	@echo "Usage: make test-module MODULE=app.core.recommendation"
	@if [ -z "$(MODULE)" ]; then \
		echo "Please specify MODULE=path.to.module"; \
		exit 1; \
	fi
	python -m pytest tests/ -v -k "$(MODULE)"

# Run tests in parallel (if pytest-xdist is installed)
test-parallel:
	@echo "Running tests in parallel..."
	python -m pytest tests/ -n auto

# Show test structure
test-structure:
	@echo "Test directory structure:"
	@tree tests/ -I "__pycache__" || find tests/ -type f -name "*.py" | sort

# Validate test organization
validate-tests:
	@echo "Validating test organization..."
	@echo "Checking for test files in correct directories..."
	@if [ ! -f "tests/unit/test_recommendation_unit.py" ]; then \
		echo "Missing: tests/unit/test_recommendation_unit.py"; \
	else \
		echo "Found: tests/unit/test_recommendation_unit.py"; \
	fi
	@if [ ! -f "tests/integration/test_json_output.py" ]; then \
		echo "Missing: tests/integration/test_json_output.py"; \
	else \
		echo "Found: tests/integration/test_json_output.py"; \
	fi
	@if [ ! -f "tests/integration/test_recommendation.py" ]; then \
		echo "Missing: tests/integration/test_recommendation.py"; \
	else \
		echo "Found: tests/integration/test_recommendation.py"; \
	fi
	@if [ ! -f "tests/rag/test_rag_pipeline.py" ]; then \
		echo "Missing: tests/rag/test_rag_pipeline.py"; \
	else \
		echo "Found: tests/rag/test_rag_pipeline.py"; \
	fi
	@if [ ! -f "tests/utils/test_document_loading.py" ]; then \
		echo "Missing: tests/utils/test_document_loading.py"; \
	else \
		echo "Found: tests/utils/test_document_loading.py"; \
	fi
	@if [ ! -f "tests/utils/rebuild_vectorstore.py" ]; then \
		echo "Missing: tests/utils/rebuild_vectorstore.py"; \
	else \
		echo "Found: tests/utils/rebuild_vectorstore.py"; \
	fi
	@echo "Test organization validation complete!" 