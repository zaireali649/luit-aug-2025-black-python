#!/usr/bin/env python3
"""
Test runner script for luit-aug-2025-black-python project.

This script provides multiple ways to run the test suite:
1. Run all tests
2. Run tests with coverage reporting
3. Run specific test modules
4. Run tests in verbose mode

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --coverage         # Run with coverage report
    python run_tests.py --verbose          # Run in verbose mode
    python run_tests.py --module <name>    # Run specific test module
    python run_tests.py --help            # Show help
"""

import argparse
import sys
import unittest
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def discover_tests(test_dir="tests/unit", pattern="test_*.py"):
    """
    Discover and return test suite from the specified directory.
    
    Args:
        test_dir (str): Directory containing test files
        pattern (str): Pattern to match test files
        
    Returns:
        unittest.TestSuite: Test suite containing discovered tests
    """
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern=pattern)
    return suite


def run_specific_module(module_name):
    """
    Run tests from a specific module.
    
    Args:
        module_name (str): Name of the test module (without test_ prefix)
        
    Returns:
        unittest.TestResult: Test results
    """
    # Add test_ prefix if not present
    if not module_name.startswith('test_'):
        module_name = f'test_{module_name}'
    
    # Remove .py extension if present
    if module_name.endswith('.py'):
        module_name = module_name[:-3]
    
    try:
        # Import the specific test module
        test_module = __import__(f'tests.unit.{module_name}', fromlist=[''])
        
        # Create test suite from the module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)
        
        # Run the tests
        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)
    
    except ImportError as e:
        print(f"Error: Could not import test module '{module_name}': {e}")
        sys.exit(1)


def run_with_coverage():
    """
    Run tests with coverage reporting.
    
    Returns:
        unittest.TestResult: Test results
    """
    try:
        import coverage
    except ImportError:
        print("Error: coverage package not installed.")
        print("Install it with: pip install coverage")
        sys.exit(1)
    
    # Start coverage
    cov = coverage.Coverage()
    cov.start()
    
    try:
        # Run tests
        suite = discover_tests()
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        
        print("\n" + "="*50)
        print("COVERAGE REPORT")
        print("="*50)
        cov.report(show_missing=True)
        
        # Generate HTML report
        html_dir = "htmlcov"
        cov.html_report(directory=html_dir)
        print(f"\nDetailed HTML coverage report generated in '{html_dir}/' directory")
        
        return result
        
    except Exception as e:
        cov.stop()
        print(f"Error during coverage testing: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Run unit tests for luit-aug-2025-black-python project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py                         # Run all tests
    python run_tests.py --coverage              # Run with coverage
    python run_tests.py --verbose               # Verbose output
    python run_tests.py --module hello_world    # Run specific module
    python run_tests.py --module test_helpers   # Run helpers tests
        """
    )
    
    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='Run tests with coverage reporting'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Run tests in verbose mode'
    )
    
    parser.add_argument(
        '--module', '-m',
        type=str,
        help='Run tests for a specific module (e.g., hello_world, helpers)'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available test modules'
    )
    
    args = parser.parse_args()
    
    # List available test modules
    if args.list:
        test_dir = Path("tests/unit")
        if test_dir.exists():
            test_files = list(test_dir.glob("test_*.py"))
            print("Available test modules:")
            for test_file in sorted(test_files):
                module_name = test_file.stem[5:]  # Remove 'test_' prefix
                print(f"  {module_name}")
        else:
            print("No test directory found.")
        return
    
    # Change to project directory
    os.chdir(project_root)
    
    # Run specific module tests
    if args.module:
        print(f"Running tests for module: {args.module}")
        result = run_specific_module(args.module)
        
    # Run with coverage
    elif args.coverage:
        print("Running all tests with coverage reporting...")
        result = run_with_coverage()
        
    # Run all tests
    else:
        print("Running all unit tests...")
        suite = discover_tests()
        verbosity = 2 if args.verbose else 1
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
    
    # Print summary
    if hasattr(result, 'testsRun'):
        print("\n" + "="*50)
        print("TEST SUMMARY")
        print("="*50)
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        
        if result.failures:
            print(f"\nFAILURES ({len(result.failures)}):")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if result.errors:
            print(f"\nERRORS ({len(result.errors)}):")
            for test, traceback in result.errors:
                print(f"  - {test}")
        
        # Exit with error code if tests failed
        if result.failures or result.errors:
            print("\n❌ Some tests failed!")
            sys.exit(1)
        else:
            print("\n✅ All tests passed!")
            sys.exit(0)


if __name__ == '__main__':
    main()
