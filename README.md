# luit-aug-2025-black-python

A collaborative repository for the **Level Up In Tech – August 2025 Black Python Cohort** to practice and grow Python skills through lessons, exercises, and projects.

## 📋 Table of Contents

- [Setup](#setup)
- [Project Structure](#project-structure)
- [Scripts Overview](#scripts-overview)
- [AWS Resources](#aws-resources)
- [Dependencies](#dependencies)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contributing](#contributing)

## 🚀 Setup

### Prerequisites
- Python 3.7 or higher
- AWS CLI configured with appropriate credentials
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd luit-aug-2025-black-python
```

2. Install required dependencies:
```bash
pip install -r .\requirements.txt
```

3. Ensure AWS credentials are configured:
```bash
aws configure
```

## 📁 Project Structure

```
luit-aug-2025-black-python/
├── creating_instances.py      # EC2 instance creation with multiple AMI types
├── data_type_fun.py          # Python data types and string manipulation examples
├── hello_world.py            # Basic Python "Hello World" example
├── helpers.py                # AWS utility functions and EC2/S3 client helpers
├── list_buckets.py           # Simple S3 bucket listing script
├── list_vpc_ids.py           # VPC ID enumeration script
├── listing_resources.py      # Comprehensive AWS resource listing
├── using_imports.py          # Demonstration of Python imports and libraries
├── lambdas/
│   └── list_buckets/
│       └── lambda_function.py # AWS Lambda function for S3 bucket listing
├── requirements.txt          # Python package dependencies
└── README.md                # This documentation file
```

## 📜 Scripts Overview

### Core Learning Files

- **`hello_world.py`** - Introduction to Python basics with simple print statements and functions
- **`data_type_fun.py`** - Comprehensive examples of Python data types, string manipulation, and type casting
- **`using_imports.py`** - Demonstrates importing built-in modules, custom modules, and third-party packages

### AWS Integration Scripts

- **`helpers.py`** - Central utility module containing AWS client creation and resource management functions
- **`creating_instances.py`** - Advanced EC2 instance provisioning with support for Ubuntu, Amazon Linux 2023, and Amazon Linux 2 AMIs
- **`list_buckets.py`** - Simple S3 bucket enumeration using boto3
- **`list_vpc_ids.py`** - VPC discovery and ID listing functionality
- **`listing_resources.py`** - Comprehensive AWS resource inventory script

### Serverless Components

- **`lambdas/list_buckets/lambda_function.py`** - Production-ready AWS Lambda function for S3 bucket listing with proper error handling and JSON responses

## ☁️ AWS Resources

This project interacts with the following AWS services:

- **Amazon EC2**: Instance creation and management
- **Amazon S3**: Bucket listing and management
- **Amazon VPC**: Virtual Private Cloud enumeration
- **AWS Lambda**: Serverless function execution

### Required AWS Permissions

Ensure your AWS credentials have the following permissions:
- `ec2:DescribeInstances`
- `ec2:RunInstances`
- `ec2:DescribeVpcs`
- `s3:ListAllMyBuckets`

## 📦 Dependencies

The project requires the following Python packages (defined in `requirements.txt`):

- **`matplotlib`** - Data visualization and plotting library
- **`pyfiglet`** - ASCII art text generation

AWS integration relies on:
- **`boto3`** - AWS SDK for Python (typically pre-installed in AWS environments)

## 💡 Usage Examples

### Running Individual Scripts

```bash
# Basic Python examples
python hello_world.py
python data_type_fun.py

# AWS resource enumeration
python list_buckets.py
python list_vpc_ids.py
python listing_resources.py

# EC2 instance creation (use with caution - creates billable resources)
python creating_instances.py

# Import demonstrations with visualizations
python using_imports.py
```

### Using Helper Functions

```python
from helpers import get_ec2_client, get_s3_client, list_buckets

# Create AWS clients
ec2 = get_ec2_client()
s3 = get_s3_client()

# List S3 buckets
buckets = list_buckets(s3)
print(buckets)
```

### Deploying Lambda Function

```bash
# Package and deploy the Lambda function
cd lambdas/list_buckets
zip -r function.zip .
aws lambda create-function --function-name list-buckets \
  --zip-file fileb://function.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/lambda-execution-role
```

## 🧪 Testing

This project includes comprehensive unit tests for all Python modules to ensure code quality and reliability.

### Test Structure

```
tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_hello_world.py          # Tests for hello_world.py
│   ├── test_helpers.py              # Tests for helpers.py (AWS functions)
│   ├── test_creating_instances.py   # Tests for creating_instances.py
│   ├── test_listing_resources.py    # Tests for listing_resources.py
│   └── test_lambda_function.py      # Tests for Lambda function
└── run_tests.py                     # Test runner script
```

### Running Tests

#### Install Testing Dependencies

First, ensure all testing dependencies are installed:

```bash
pip install -r .\requirements.txt
```

#### Run All Tests

```bash
# Basic test run
python run_tests.py

# Verbose output
python run_tests.py --verbose
```

#### Run Specific Test Modules

```bash
# Test a specific module
python run_tests.py --module hello_world
python run_tests.py --module helpers
python run_tests.py --module lambda_function

# List available test modules
python run_tests.py --list
```

#### Run Tests with Coverage

```bash
# Generate coverage report
python run_tests.py --coverage
```

This will generate:
- Console coverage report
- HTML coverage report in `htmlcov/` directory

#### Alternative Test Runners

You can also use standard Python unittest or pytest:

```bash
# Using unittest
python -m unittest discover tests/unit

# Using pytest (if installed)
pytest tests/unit/

# Using pytest with coverage
pytest tests/unit/ --cov=. --cov-report=html
```

### Test Features

- **Comprehensive Coverage**: Tests cover all functions and edge cases
- **AWS Mocking**: Uses `moto` and `unittest.mock` to avoid actual AWS API calls
- **Isolated Tests**: Each test is independent and doesn't affect others
- **Multiple Scenarios**: Tests include success cases, edge cases, and error conditions
- **Print Statement Verification**: Tests verify console output where applicable

### Testing Dependencies

The following packages are used for testing:

- **`boto3`** - AWS SDK (already required for main functionality)
- **`moto[s3,ec2]`** - AWS service mocking for testing
- **`coverage`** - Code coverage measurement
- **`pytest`** - Alternative test runner (optional)
- **`pytest-cov`** - Coverage plugin for pytest (optional)

## 🤝 Contributing

This is a collaborative learning environment. When contributing:

1. Follow Python PEP 8 style guidelines
2. Include comprehensive docstrings for all functions
3. Test AWS scripts in development environments before production
4. Update documentation for new features
5. Be mindful of AWS costs when creating resources

## ⚠️ Important Notes

- **AWS Costs**: Scripts that create EC2 instances will incur AWS charges. Always terminate resources when not needed.
- **Security**: Never commit AWS credentials to the repository. Use IAM roles, environment variables, or AWS credential files.
- **Region**: Scripts use the default AWS region from your configuration. Ensure this is set appropriately.

---

**Happy Learning! 🐍☁️**