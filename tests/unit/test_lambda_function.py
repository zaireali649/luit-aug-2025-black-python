"""
Unit tests for lambdas/list_buckets/lambda_function.py module.

This module contains tests for AWS Lambda function with proper mocking
to avoid actual AWS API calls during testing.
"""

import unittest
from unittest.mock import patch, Mock
import json
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import the lambda function
from lambdas.list_buckets import lambda_function


class TestLambdaFunction(unittest.TestCase):
    """Test cases for lambda_function.py AWS Lambda handler."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_event = {}
        self.test_context = Mock()

    @patch('lambdas.list_buckets.lambda_function.boto3')
    @patch('builtins.print')
    def test_lambda_handler_success(self, mock_print, mock_boto3):
        """Test successful lambda handler execution."""
        # Mock S3 client and response
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client
        
        mock_response = {
            'Buckets': [
                {'Name': 'bucket1', 'CreationDate': '2023-01-01'},
                {'Name': 'bucket2', 'CreationDate': '2023-01-02'},
                {'Name': 'bucket3', 'CreationDate': '2023-01-03'}
            ]
        }
        mock_s3_client.list_buckets.return_value = mock_response
        
        # Call the lambda handler
        result = lambda_function.lambda_handler(self.test_event, self.test_context)
        
        # Verify boto3.client was called with 's3'
        mock_boto3.client.assert_called_once_with('s3')
        
        # Verify list_buckets was called
        mock_s3_client.list_buckets.assert_called_once()
        
        # Verify print statements for each bucket
        expected_print_calls = [
            unittest.mock.call('bucket1'),
            unittest.mock.call('bucket2'),
            unittest.mock.call('bucket3')
        ]
        mock_print.assert_has_calls(expected_print_calls)
        
        # Verify the response structure
        self.assertEqual(result['statusCode'], 200)
        
        # Parse the JSON body and verify bucket names
        response_body = json.loads(result['body'])
        expected_bucket_names = ['bucket1', 'bucket2', 'bucket3']
        self.assertEqual(response_body, expected_bucket_names)

    @patch('lambdas.list_buckets.lambda_function.boto3')
    @patch('builtins.print')
    def test_lambda_handler_empty_buckets(self, mock_print, mock_boto3):
        """Test lambda handler with empty bucket list."""
        # Mock S3 client and response
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client
        
        mock_response = {'Buckets': []}
        mock_s3_client.list_buckets.return_value = mock_response
        
        # Call the lambda handler
        result = lambda_function.lambda_handler(self.test_event, self.test_context)
        
        # Verify API calls
        mock_boto3.client.assert_called_once_with('s3')
        mock_s3_client.list_buckets.assert_called_once()
        
        # Verify no bucket names were printed
        mock_print.assert_not_called()
        
        # Verify the response
        self.assertEqual(result['statusCode'], 200)
        response_body = json.loads(result['body'])
        self.assertEqual(response_body, [])

    @patch('lambdas.list_buckets.lambda_function.boto3')
    @patch('builtins.print')
    def test_lambda_handler_single_bucket(self, mock_print, mock_boto3):
        """Test lambda handler with single bucket."""
        # Mock S3 client and response
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client
        
        mock_response = {
            'Buckets': [
                {'Name': 'single-bucket', 'CreationDate': '2023-01-01'}
            ]
        }
        mock_s3_client.list_buckets.return_value = mock_response
        
        # Call the lambda handler
        result = lambda_function.lambda_handler(self.test_event, self.test_context)
        
        # Verify print was called once
        mock_print.assert_called_once_with('single-bucket')
        
        # Verify the response
        self.assertEqual(result['statusCode'], 200)
        response_body = json.loads(result['body'])
        self.assertEqual(response_body, ['single-bucket'])

    def test_lambda_handler_event_and_context_ignored(self):
        """Test that event and context parameters are properly ignored."""
        # Test with various event and context values
        test_cases = [
            ({}, None),
            ({'key': 'value'}, Mock()),
            ({'Records': []}, Mock()),
            (None, Mock())
        ]
        
        for event, context in test_cases:
            with self.subTest(event=event, context=context):
                with patch('lambdas.list_buckets.lambda_function.boto3') as mock_boto3:
                    mock_s3_client = Mock()
                    mock_boto3.client.return_value = mock_s3_client
                    mock_s3_client.list_buckets.return_value = {'Buckets': []}
                    
                    # Should not raise any errors
                    result = lambda_function.lambda_handler(event, context)
                    self.assertEqual(result['statusCode'], 200)

    @patch('lambdas.list_buckets.lambda_function.boto3')
    def test_lambda_handler_response_format(self, mock_boto3):
        """Test that the lambda handler returns the correct response format."""
        # Mock S3 client and response
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client
        
        mock_response = {
            'Buckets': [
                {'Name': 'test-bucket', 'CreationDate': '2023-01-01'}
            ]
        }
        mock_s3_client.list_buckets.return_value = mock_response
        
        result = lambda_function.lambda_handler({}, None)
        
        # Verify response structure
        self.assertIsInstance(result, dict)
        self.assertIn('statusCode', result)
        self.assertIn('body', result)
        
        # Verify status code
        self.assertEqual(result['statusCode'], 200)
        
        # Verify body is valid JSON
        self.assertIsInstance(result['body'], str)
        parsed_body = json.loads(result['body'])
        self.assertIsInstance(parsed_body, list)

    @patch('lambdas.list_buckets.lambda_function.boto3')
    def test_lambda_handler_json_formatting(self, mock_boto3):
        """Test that the JSON response is properly formatted with indentation."""
        # Mock S3 client and response
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client
        
        mock_response = {
            'Buckets': [
                {'Name': 'bucket1', 'CreationDate': '2023-01-01'},
                {'Name': 'bucket2', 'CreationDate': '2023-01-02'}
            ]
        }
        mock_s3_client.list_buckets.return_value = mock_response
        
        result = lambda_function.lambda_handler({}, None)
        
        # Verify that the JSON is formatted with indentation
        expected_json = json.dumps(['bucket1', 'bucket2'], indent=4)
        self.assertEqual(result['body'], expected_json)

    def test_function_docstring_and_typing(self):
        """Test that the function has proper documentation and type hints."""
        import inspect
        
        # Check function signature
        sig = inspect.signature(lambda_function.lambda_handler)
        params = list(sig.parameters.keys())
        self.assertEqual(params, ['event', 'context'])
        
        # Check that function has a docstring
        self.assertIsNotNone(lambda_function.lambda_handler.__doc__)
        self.assertIn('AWS Lambda handler', lambda_function.lambda_handler.__doc__)

    @patch('lambdas.list_buckets.lambda_function.boto3')
    def test_bucket_iteration_logic(self, mock_boto3):
        """Test the bucket iteration and name extraction logic."""
        mock_s3_client = Mock()
        mock_boto3.client.return_value = mock_s3_client
        
        # Test with buckets that have additional metadata
        mock_response = {
            'Buckets': [
                {
                    'Name': 'bucket1',
                    'CreationDate': '2023-01-01',
                    'ExtraField': 'should_be_ignored'
                },
                {
                    'Name': 'bucket2',
                    'CreationDate': '2023-01-02',
                    'AnotherField': 'also_ignored'
                }
            ]
        }
        mock_s3_client.list_buckets.return_value = mock_response
        
        result = lambda_function.lambda_handler({}, None)
        
        # Verify only bucket names are returned, ignoring other metadata
        response_body = json.loads(result['body'])
        self.assertEqual(response_body, ['bucket1', 'bucket2'])


if __name__ == '__main__':
    unittest.main()
