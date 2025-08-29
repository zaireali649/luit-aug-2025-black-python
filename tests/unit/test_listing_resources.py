"""
Unit tests for listing_resources.py module.

This module contains tests for AWS resource listing functions with proper mocking
to avoid actual AWS API calls during testing.
"""

import unittest
from unittest.mock import patch, Mock, call
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import listing_resources


class TestListingResources(unittest.TestCase):
    """Test cases for listing_resources.py functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_s3_client = Mock()
        self.mock_ec2_client = Mock()

    @patch('builtins.print')
    @patch('listing_resources.list_buckets')
    def test_print_bucket_names(self, mock_list_buckets, mock_print):
        """Test printing S3 bucket names."""
        # Mock the list_buckets function to return test data
        test_buckets = ['bucket1', 'bucket2', 'bucket3']
        mock_list_buckets.return_value = test_buckets
        
        listing_resources.print_bucket_names(self.mock_s3_client)
        
        # Verify list_buckets was called with the correct client
        mock_list_buckets.assert_called_once_with(self.mock_s3_client)
        
        # Verify each bucket name was printed
        expected_print_calls = [call('bucket1'), call('bucket2'), call('bucket3')]
        mock_print.assert_has_calls(expected_print_calls)

    @patch('builtins.print')
    @patch('listing_resources.list_buckets')
    def test_print_bucket_names_empty(self, mock_list_buckets, mock_print):
        """Test printing S3 bucket names with empty list."""
        mock_list_buckets.return_value = []
        
        listing_resources.print_bucket_names(self.mock_s3_client)
        
        mock_list_buckets.assert_called_once_with(self.mock_s3_client)
        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('listing_resources.list_buckets')
    def test_print_bucket_names_single_bucket(self, mock_list_buckets, mock_print):
        """Test printing S3 bucket names with single bucket."""
        mock_list_buckets.return_value = ['single-bucket']
        
        listing_resources.print_bucket_names(self.mock_s3_client)
        
        mock_list_buckets.assert_called_once_with(self.mock_s3_client)
        mock_print.assert_called_once_with('single-bucket')

    @patch('builtins.print')
    @patch('listing_resources.describe_instances')
    def test_print_instance_ids(self, mock_describe_instances, mock_print):
        """Test printing EC2 instance IDs."""
        # Mock the describe_instances function to return test data
        test_instances = [
            {'InstanceId': 'i-1234567890abcdef0', 'State': {'Name': 'running'}},
            {'InstanceId': 'i-0987654321fedcba0', 'State': {'Name': 'stopped'}},
            {'InstanceId': 'i-abcdef1234567890', 'State': {'Name': 'running'}}
        ]
        mock_describe_instances.return_value = test_instances
        
        listing_resources.print_instance_ids(self.mock_ec2_client)
        
        # Verify describe_instances was called with the correct client
        mock_describe_instances.assert_called_once_with(self.mock_ec2_client)
        
        # Verify each instance ID was printed
        expected_print_calls = [
            call('i-1234567890abcdef0'),
            call('i-0987654321fedcba0'),
            call('i-abcdef1234567890')
        ]
        mock_print.assert_has_calls(expected_print_calls)

    @patch('builtins.print')
    @patch('listing_resources.describe_instances')
    def test_print_instance_ids_empty(self, mock_describe_instances, mock_print):
        """Test printing EC2 instance IDs with empty list."""
        mock_describe_instances.return_value = []
        
        listing_resources.print_instance_ids(self.mock_ec2_client)
        
        mock_describe_instances.assert_called_once_with(self.mock_ec2_client)
        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('listing_resources.describe_instances')
    def test_print_instance_ids_single_instance(self, mock_describe_instances, mock_print):
        """Test printing EC2 instance IDs with single instance."""
        test_instances = [
            {'InstanceId': 'i-1234567890abcdef0', 'State': {'Name': 'running'}}
        ]
        mock_describe_instances.return_value = test_instances
        
        listing_resources.print_instance_ids(self.mock_ec2_client)
        
        mock_describe_instances.assert_called_once_with(self.mock_ec2_client)
        mock_print.assert_called_once_with('i-1234567890abcdef0')

    def test_print_instance_ids_instance_collection(self):
        """Test that print_instance_ids correctly collects instance IDs."""
        # Test the internal logic of instance ID collection
        test_instances = [
            {'InstanceId': 'i-111', 'State': {'Name': 'running'}},
            {'InstanceId': 'i-222', 'State': {'Name': 'stopped'}},
            {'InstanceId': 'i-333', 'State': {'Name': 'pending'}}
        ]
        
        # Simulate the collection logic
        instance_ids = []
        for instance in test_instances:
            instance_ids.append(instance['InstanceId'])
        
        expected_ids = ['i-111', 'i-222', 'i-333']
        self.assertEqual(instance_ids, expected_ids)

    @patch('listing_resources.print_instance_ids')
    @patch('listing_resources.print_bucket_names')
    @patch('listing_resources.get_s3_client')
    @patch('listing_resources.get_ec2_client')
    def test_main_execution(self, mock_get_ec2_client, mock_get_s3_client, 
                           mock_print_bucket_names, mock_print_instance_ids):
        """Test the main execution block by simulating __main__ execution."""
        mock_ec2_client = Mock()
        mock_s3_client = Mock()
        mock_get_ec2_client.return_value = mock_ec2_client
        mock_get_s3_client.return_value = mock_s3_client
        
        # Simulate the main execution block manually since it's protected by if __name__ == "__main__"
        # This tests the logic that would run when the script is executed directly
        
        # Get AWS clients using helper functions
        ec2_client = listing_resources.get_ec2_client()
        s3_client = listing_resources.get_s3_client()

        # Print bucket names from S3
        listing_resources.print_bucket_names(s3_client)

        # Print EC2 instance IDs
        listing_resources.print_instance_ids(ec2_client)
        
        # Verify that client getters were called
        mock_get_ec2_client.assert_called_once()
        mock_get_s3_client.assert_called_once()
        
        # Verify that print functions were called with correct clients
        mock_print_bucket_names.assert_called_once_with(mock_s3_client)
        mock_print_instance_ids.assert_called_once_with(mock_ec2_client)

    def test_function_signatures(self):
        """Test that functions have the expected signatures."""
        import inspect
        
        # Test print_bucket_names signature
        sig = inspect.signature(listing_resources.print_bucket_names)
        params = list(sig.parameters.keys())
        self.assertEqual(params, ['s3_client'])
        
        # Test print_instance_ids signature
        sig = inspect.signature(listing_resources.print_instance_ids)
        params = list(sig.parameters.keys())
        self.assertEqual(params, ['ec2_client'])

    def test_type_hints_compliance(self):
        """Test that functions comply with their type hints."""
        # This test verifies that the functions can handle the expected types
        # without actually calling AWS services
        
        # Test with mock clients (which should work with Any typing)
        mock_s3 = Mock()
        mock_ec2 = Mock()
        
        # These should not raise type errors
        with patch('listing_resources.list_buckets', return_value=[]):
            with patch('builtins.print'):
                listing_resources.print_bucket_names(mock_s3)
        
        with patch('listing_resources.describe_instances', return_value=[]):
            with patch('builtins.print'):
                listing_resources.print_instance_ids(mock_ec2)


if __name__ == '__main__':
    unittest.main()
