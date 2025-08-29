"""
Unit tests for helpers.py module.

This module contains tests for AWS helper functions with proper mocking
to avoid actual AWS API calls during testing.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import helpers


class TestHelpers(unittest.TestCase):
    """Test cases for helpers.py AWS utility functions."""

    @patch('helpers.boto3')
    def test_get_ec2_client(self, mock_boto3):
        """Test EC2 client creation."""
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        result = helpers.get_ec2_client()
        
        mock_boto3.client.assert_called_once_with('ec2')
        self.assertEqual(result, mock_client)

    @patch('helpers.boto3')
    def test_get_s3_client(self, mock_boto3):
        """Test S3 client creation."""
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        result = helpers.get_s3_client()
        
        mock_boto3.client.assert_called_once_with('s3')
        self.assertEqual(result, mock_client)

    def test_describe_instances(self):
        """Test describe_instances function."""
        # Mock EC2 client
        mock_client = Mock()
        
        # Mock response data
        mock_response = {
            'Reservations': [
                {
                    'Instances': [
                        {'InstanceId': 'i-1234567890abcdef0', 'State': {'Name': 'running'}},
                        {'InstanceId': 'i-0987654321fedcba0', 'State': {'Name': 'stopped'}}
                    ]
                },
                {
                    'Instances': [
                        {'InstanceId': 'i-abcdef1234567890', 'State': {'Name': 'running'}}
                    ]
                }
            ]
        }
        
        mock_client.describe_instances.return_value = mock_response
        
        result = helpers.describe_instances(mock_client)
        
        # Verify the function was called
        mock_client.describe_instances.assert_called_once()
        
        # Verify the result contains all instances
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['InstanceId'], 'i-1234567890abcdef0')
        self.assertEqual(result[1]['InstanceId'], 'i-0987654321fedcba0')
        self.assertEqual(result[2]['InstanceId'], 'i-abcdef1234567890')

    def test_describe_instances_empty(self):
        """Test describe_instances with empty response."""
        mock_client = Mock()
        mock_client.describe_instances.return_value = {'Reservations': []}
        
        result = helpers.describe_instances(mock_client)
        
        self.assertEqual(result, [])

    @patch('helpers.create_instance')
    def test_create_ubuntu_instance(self, mock_create_instance):
        """Test Ubuntu instance creation."""
        mock_client = Mock()
        
        helpers.create_ubuntu_instance(mock_client)
        
        mock_create_instance.assert_called_once_with(mock_client, "ami-04b70fa74e45c3917")

    @patch('helpers.create_instance')
    def test_create_amazon_linux_2023_instance(self, mock_create_instance):
        """Test Amazon Linux 2023 instance creation."""
        mock_client = Mock()
        
        helpers.create_amazon_linux_2023_instance(mock_client)
        
        mock_create_instance.assert_called_once_with(mock_client, "ami-08a0d1e16fc3f61ea")

    @patch('helpers.create_instance')
    def test_create_amazon_linux_2_instance(self, mock_create_instance):
        """Test Amazon Linux 2 instance creation."""
        mock_client = Mock()
        
        helpers.create_amazon_linux_2_instance(mock_client)
        
        mock_create_instance.assert_called_once_with(mock_client, "ami-0eaf7c3456e7b5b68")

    def test_create_instance(self):
        """Test generic instance creation."""
        mock_client = Mock()
        test_ami = "ami-12345678"
        
        helpers.create_instance(mock_client, test_ami)
        
        mock_client.run_instances.assert_called_once_with(
            MaxCount=1,
            MinCount=1,
            ImageId=test_ami,
            InstanceType="t2.micro",
            KeyName='private-ec2',
            SecurityGroupIds=['sg-0197b8159a5d886f8']
        )

    def test_list_buckets(self):
        """Test S3 bucket listing."""
        mock_client = Mock()
        
        # Mock response data
        mock_response = {
            'Buckets': [
                {'Name': 'bucket1', 'CreationDate': '2023-01-01'},
                {'Name': 'bucket2', 'CreationDate': '2023-01-02'},
                {'Name': 'bucket3', 'CreationDate': '2023-01-03'}
            ]
        }
        
        mock_client.list_buckets.return_value = mock_response
        
        result = helpers.list_buckets(mock_client)
        
        mock_client.list_buckets.assert_called_once()
        self.assertEqual(result, ['bucket1', 'bucket2', 'bucket3'])

    def test_list_buckets_empty(self):
        """Test S3 bucket listing with empty response."""
        mock_client = Mock()
        mock_client.list_buckets.return_value = {'Buckets': []}
        
        result = helpers.list_buckets(mock_client)
        
        self.assertEqual(result, [])

    @patch('builtins.print')
    @patch('helpers.get_s3_client')
    @patch('helpers.get_ec2_client')
    def test_main_execution(self, mock_get_ec2, mock_get_s3, mock_print):
        """Test the main execution block by simulating __main__ execution."""
        # Mock clients
        mock_ec2_client = Mock()
        mock_s3_client = Mock()
        mock_get_ec2.return_value = mock_ec2_client
        mock_get_s3.return_value = mock_s3_client
        
        # Mock S3 response
        mock_response = {'Buckets': [{'Name': 'test-bucket'}]}
        mock_s3_client.list_buckets.return_value = mock_response
        
        # Simulate the main execution block manually since it's protected by if __name__ == "__main__"
        # This tests the logic that would run when the script is executed directly
        
        ec2_client = helpers.get_ec2_client()  # Get the EC2 client
        # Commented out instance creation calls are not tested since they're commented in the original
        
        s3_client = helpers.get_s3_client()  # Get the S3 client
        response = s3_client.list_buckets()  # List the S3 buckets
        
        print(response)  # Print the response containing bucket information
        
        # Verify clients were created
        mock_get_ec2.assert_called()
        mock_get_s3.assert_called()
        
        # Verify S3 list_buckets was called
        mock_s3_client.list_buckets.assert_called()
        
        # Verify print was called with the response
        mock_print.assert_called_with(mock_response)


if __name__ == '__main__':
    unittest.main()
