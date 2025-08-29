"""
Unit tests for hello_world.py module.

This module contains tests for the basic functions in hello_world.py,
demonstrating how to test simple Python functions with output verification.
"""

import unittest
from unittest.mock import patch
import sys
import os

# Add the project root to the Python path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import hello_world


class TestHelloWorld(unittest.TestCase):
    """Test cases for hello_world.py functions."""

    @patch('builtins.print')
    def test_say_hello(self, mock_print):
        """Test that say_hello() prints the correct message."""
        hello_world.say_hello()
        mock_print.assert_called_once_with("Hello.")

    @patch('builtins.print')
    def test_main_script_execution(self, mock_print):
        """Test the main script execution by importing and checking print calls."""
        # Since hello_world.py executes print("Hello World") on import,
        # we need to reload the module to test it
        import importlib
        importlib.reload(hello_world)
        
        # Check if "Hello World" was printed during module import
        mock_print.assert_any_call("Hello World")

    def test_say_hello_returns_none(self):
        """Test that say_hello() returns None."""
        result = hello_world.say_hello()
        self.assertIsNone(result)

    def test_say_hello_function_exists(self):
        """Test that say_hello function exists and is callable."""
        self.assertTrue(hasattr(hello_world, 'say_hello'))
        self.assertTrue(callable(hello_world.say_hello))


if __name__ == '__main__':
    unittest.main()
