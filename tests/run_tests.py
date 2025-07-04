#!/usr/bin/env python3
"""
Test runner script for the nutrition app.
Provides easy access to run different categories of tests.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False

def run_pytest_tests(test_path, description):
    """Run pytest tests with proper configuration."""
    command = f"python -m pytest {test_path} -v"
    return run_command(command, description)

def run_utility_script(script_path, description):
    """Run a utility script."""
    command = f"python {script_path}"
    return run_command(command, description)

def main():
    parser = argparse.ArgumentParser(description="Run nutrition app tests by category")
    parser.add_argument(
        "category",
        choices=["all", "unit", "integration", "rag", "utils", "document-loading", "rebuild-vectorstore"],
        help="Test category to run"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Run with verbose output"
    )
    
    args = parser.parse_args()
    
    # Get the tests directory
    tests_dir = Path(__file__).parent
    
    if args.category == "all":
        print("Running all test categories...")
        success = True
        
        # Run unit tests
        success &= run_pytest_tests(
            tests_dir / "unit",
            "Unit Tests"
        )
        
        # Run integration tests
        success &= run_pytest_tests(
            tests_dir / "integration",
            "Integration Tests"
        )
        
        # Run RAG tests
        success &= run_pytest_tests(
            tests_dir / "rag",
            "RAG Pipeline Tests"
        )
        
        if success:
            print("\n🎉 All test categories completed successfully!")
        else:
            print("\n⚠️  Some test categories failed. Check the output above.")
            sys.exit(1)
    
    elif args.category == "unit":
        run_pytest_tests(tests_dir / "unit", "Unit Tests")
    
    elif args.category == "integration":
        run_pytest_tests(tests_dir / "integration", "Integration Tests")
    
    elif args.category == "rag":
        run_pytest_tests(tests_dir / "rag", "RAG Pipeline Tests")
    
    elif args.category == "utils":
        print("Running utility scripts...")
        success = True
        
        # Test document loading
        success &= run_utility_script(
            tests_dir / "utils" / "test_document_loading.py",
            "Document Loading Test"
        )
        
        # Rebuild vector store
        success &= run_utility_script(
            tests_dir / "utils" / "rebuild_vectorstore.py",
            "Vector Store Rebuild"
        )
        
        if success:
            print("\n🎉 All utility scripts completed successfully!")
        else:
            print("\n⚠️  Some utility scripts failed. Check the output above.")
            sys.exit(1)
    
    elif args.category == "document-loading":
        run_utility_script(
            tests_dir / "utils" / "test_document_loading.py",
            "Document Loading Test"
        )
    
    elif args.category == "rebuild-vectorstore":
        run_utility_script(
            tests_dir / "utils" / "rebuild_vectorstore.py",
            "Vector Store Rebuild"
        )

if __name__ == "__main__":
    main() 