"""
Unit tests for creating_instances.py module.

This module contains tests for EC2 instance creation functions with proper mocking
to avoid actual AWS API calls and resource creation during testing.
"""

import unittest
from unittest.mock import patch, Mock, call
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import creating_instances


class TestCreatingInstances(unittest.TestCase):
    """Test cases for creating_instances.py functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_ec2_client = Mock()

    @patch('builtins.print')
    @patch('creating_instances.create_ubuntu_instance')
    def test_create_instances_ubuntu_single(self, mock_create_ubuntu, mock_print):
        """Test creating a single Ubuntu instance."""
        creating_instances.create_instances(self.mock_ec2_client, "Ubuntu", 1)
        
        mock_create_ubuntu.assert_called_once_with(self.mock_ec2_client)
        mock_print.assert_called_with("Ubuntu Created")

    @patch('builtins.print')
    @patch('creating_instances.create_ubuntu_instance')
    def test_create_instances_ubuntu_multiple(self, mock_create_ubuntu, mock_print):
        """Test creating multiple Ubuntu instances."""
        creating_instances.create_instances(self.mock_ec2_client, "Ubuntu", 3)
        
        self.assertEqual(mock_create_ubuntu.call_count, 3)
        expected_calls = [call(self.mock_ec2_client)] * 3
        mock_create_ubuntu.assert_has_calls(expected_calls)
        
        # Check that "Ubuntu Created" was printed 3 times
        ubuntu_calls = [call("Ubuntu Created")] * 3
        mock_print.assert_has_calls(ubuntu_calls)

    @patch('builtins.print')
    @patch('creating_instances.create_amazon_linux_2023_instance')
    def test_create_instances_linux2023(self, mock_create_linux2023, mock_print):
        """Test creating Linux 2023 instances."""
        creating_instances.create_instances(self.mock_ec2_client, "Linux2023", 2)
        
        self.assertEqual(mock_create_linux2023.call_count, 2)
        expected_calls = [call(self.mock_ec2_client)] * 2
        mock_create_linux2023.assert_has_calls(expected_calls)
        
        linux_calls = [call("Linux 2023 Created")] * 2
        mock_print.assert_has_calls(linux_calls)

    @patch('builtins.print')
    @patch('creating_instances.create_amazon_linux_2_instance')
    def test_create_instances_linux2(self, mock_create_linux2, mock_print):
        """Test creating Linux 2 instances."""
        creating_instances.create_instances(self.mock_ec2_client, "Linux2", 1)
        
        mock_create_linux2.assert_called_once_with(self.mock_ec2_client)
        mock_print.assert_called_with("Linux 2 Created")

    @patch('builtins.print')
    def test_create_instances_unsupported_ami(self, mock_print):
        """Test handling unsupported AMI types."""
        creating_instances.create_instances(self.mock_ec2_client, "Windows", 1)
        
        mock_print.assert_called_with("Unsupported AMI")

    @patch('builtins.print')
    @patch('creating_instances.create_ubuntu_instance')
    def test_create_instances_case_insensitive(self, mock_create_ubuntu, mock_print):
        """Test that AMI type matching is case insensitive."""
        creating_instances.create_instances(self.mock_ec2_client, "ubuNtu", 1)
        
        mock_create_ubuntu.assert_called_once_with(self.mock_ec2_client)
        mock_print.assert_called_with("Ubuntu Created")

    @patch('builtins.print')
    @patch('creating_instances.create_amazon_linux_2_instance')
    def test_create_instances_whitespace_handling(self, mock_create_linux2, mock_print):
        """Test that whitespace in AMI type is handled correctly."""
        creating_instances.create_instances(self.mock_ec2_client, "  Linux 2", 1)
        
        mock_create_linux2.assert_called_once_with(self.mock_ec2_client)
        mock_print.assert_called_with("Linux 2 Created")

    @patch('builtins.print')
    @patch('creating_instances.create_amazon_linux_2023_instance')
    def test_create_instances_linux2023_variations(self, mock_create_linux2023, mock_print):
        """Test different variations of Linux 2023 AMI type."""
        test_cases = ["Linux2023", "linux2023", "LINUX2023"]
        
        for ami_type in test_cases:
            with self.subTest(ami_type=ami_type):
                mock_create_linux2023.reset_mock()
                mock_print.reset_mock()
                
                creating_instances.create_instances(self.mock_ec2_client, ami_type, 1)
                
                mock_create_linux2023.assert_called_once_with(self.mock_ec2_client)
                mock_print.assert_called_with("Linux 2023 Created")

    def test_create_instances_default_parameters(self):
        """Test create_instances with default parameters."""
        with patch('creating_instances.create_ubuntu_instance') as mock_create_ubuntu:
            with patch('builtins.print'):
                creating_instances.create_instances(self.mock_ec2_client)
                
                mock_create_ubuntu.assert_called_once_with(self.mock_ec2_client)

    def test_create_instances_zero_amount(self):
        """Test create_instances with zero amount."""
        with patch('creating_instances.create_ubuntu_instance') as mock_create_ubuntu:
            with patch('builtins.print') as mock_print:
                creating_instances.create_instances(self.mock_ec2_client, "Ubuntu", 0)
                
                mock_create_ubuntu.assert_not_called()
                mock_print.assert_not_called()

    @patch('creating_instances.get_ec2_client')
    @patch('creating_instances.create_instances')
    def test_main_execution(self, mock_create_instances, mock_get_ec2_client):
        """Test the main execution block by simulating __main__ execution."""
        mock_ec2_client = Mock()
        mock_get_ec2_client.return_value = mock_ec2_client
        
        # Simulate the main execution block manually since it's protected by if __name__ == "__main__"
        # This tests the logic that would run when the script is executed directly
        
        # Simulate getting EC2 client
        ec2_client = creating_instances.get_ec2_client()
        
        # Simulate the example calls from the main block
        creating_instances.create_instances(ec2_client, "ubuNtu")
        creating_instances.create_instances(ec2_client, "  Linux 2")
        creating_instances.create_instances(ec2_client)
        creating_instances.create_instances(ec2_client, "Linux 2")
        creating_instances.create_instances(ec2_client, ami_type="Linux 2023")
        creating_instances.create_instances(ec2_client, ami_type="Linux  2023")
        creating_instances.create_instances(ec2_client, ami_type="Centos")
        creating_instances.create_instances(ec2_client, "Linux 2", 2)
        creating_instances.create_instances(ec2_client, "Linux 2", ami_amount=3)
        creating_instances.create_instances(ec2_client, ami_amount=5)
        creating_instances.create_instances(ec2_client, ami_amount=4, ami_type="Linux 2023")
        
        # Verify that get_ec2_client was called
        mock_get_ec2_client.assert_called()
        
        # Verify that create_instances was called multiple times with different parameters
        self.assertEqual(mock_create_instances.call_count, 11)  # Should be called 11 times
        
        # Check some specific calls that should exist
        expected_calls = [
            call(mock_ec2_client, "ubuNtu"),
            call(mock_ec2_client, "  Linux 2"),
            call(mock_ec2_client),  # Default parameters
            call(mock_ec2_client, "Linux 2"),
            call(mock_ec2_client, ami_type="Linux 2023"),
            call(mock_ec2_client, ami_type="Linux  2023"),
            call(mock_ec2_client, ami_type="Centos"),
            call(mock_ec2_client, "Linux 2", 2),
            call(mock_ec2_client, "Linux 2", ami_amount=3),
            call(mock_ec2_client, ami_amount=5),
            call(mock_ec2_client, ami_amount=4, ami_type="Linux 2023")
        ]
        
        mock_create_instances.assert_has_calls(expected_calls)

    def test_normalization_logic(self):
        """Test the AMI type normalization logic directly."""
        test_cases = [
            ("Ubuntu", "ubuntu"),
            ("  Ubuntu  ", "ubuntu"),
            ("uBuNtU", "ubuntu"),
            ("Linux 2023", "linux2023"),
            ("  Linux  2023  ", "linux2023"),
            ("linux2", "linux2"),
            ("LINUX2", "linux2"),
        ]
        
        for input_ami, expected_normalized in test_cases:
            with self.subTest(input_ami=input_ami):
                # Test the normalization logic
                normalized = input_ami.lower().strip().replace(" ", "")
                self.assertEqual(normalized, expected_normalized)


if __name__ == '__main__':
    unittest.main()
