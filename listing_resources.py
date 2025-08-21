from helpers import *
import json
from typing import List, Dict, Any
import boto3


def print_bucket_names(s3_client: boto3.client) -> None:
    """
    Retrieve and print all S3 bucket names for the given client.

    Args:
        s3_client (boto3.client): A boto3 S3 client instance used to query buckets.

    Notes:
        There are multiple ways to print the list of bucket names:
        - Join with newlines: "\n".join(bucket_names)
        - Pretty-print as JSON: print(json.dumps(bucket_names, indent=4))
        - Iterate and print each bucket name individually (used here)
    """
    # Call helper function to list buckets
    bucket_names: List[str] = list_buckets(s3_client)

    # printing bucket names
    # "\n".join(bucket_names)
    # print(json.dumps(bucket_names, indent=4))
    # iterate to print bucket names
    for bucket_name in bucket_names:
        print(bucket_name)


def print_instance_ids(ec2_client: boto3.client) -> None:
    """
    Retrieve and print all EC2 instance IDs for the given client.

    Args:
        ec2_client (boto3.client): A boto3 EC2 client instance used to query instances.
    """
    # Call helper function to describe EC2 instances
    instances: List[Dict[str, Any]] = describe_instances(ec2_client)

    # Collect all instance IDs in a list
    instance_ids: List[str] = []
    for instance in instances:
        instance_ids.append(instance['InstanceId'])

    # Print each instance ID
    for instance_id in instance_ids:
        print(instance_id)


if __name__ == "__main__":
    # Get AWS clients using helper functions (likely wrappers around boto3.client)
    ec2_client = get_ec2_client()
    s3_client = get_s3_client()

    # Print bucket names from S3
    print_bucket_names(s3_client)

    # Print EC2 instance IDs
    print_instance_ids(ec2_client)
