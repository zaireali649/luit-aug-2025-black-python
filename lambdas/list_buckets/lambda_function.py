import json
import boto3  # AWS SDK for Python; used here to interact with AWS services

def lambda_handler(event: dict, context: object) -> dict:
    """
    AWS Lambda handler that lists all S3 bucket names in the account.

    Args:
        event (dict): Input event data passed by the Lambda runtime.
                      Not used in this function but required by AWS Lambda.
        context (object): AWS Lambda context object containing metadata about 
                          the invocation, function, and execution environment.
                          Not used here.

    Returns:
        dict: A dictionary with:
              - 'statusCode' (int): HTTP status code of the response.
              - 'body' (str): A JSON-formatted string containing the list of S3 bucket names.
    """

    # Create an S3 client using the Lambda's execution role credentials
    s3 = boto3.client('s3')

    # Retrieve the list of all buckets in the AWS account
    response = s3.list_buckets()

    # Extract the bucket list (each item contains metadata such as Name and CreationDate)
    buckets = response["Buckets"]

    # Initialize a list to hold bucket names only
    bucket_names: list[str] = []

    # Iterate through bucket objects, print the bucket name, and store it in the list
    for bucket in buckets:
        print(bucket["Name"])  # Logs bucket name to CloudWatch for observability
        bucket_names.append(bucket["Name"])
    
    # Return the list of bucket names as a JSON-formatted response with status code 200
    return {
        'statusCode': 200,
        'body': json.dumps(bucket_names, indent=4)
    }
