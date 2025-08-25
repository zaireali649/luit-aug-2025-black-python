import boto3  # Import the Boto3 library to interact with AWS services

def get_ec2_client() -> boto3.client:
    """
    Creates and returns an EC2 client using Boto3.

    Returns:
        boto3.client: The EC2 client.
    """
    return boto3.client('ec2')

def get_s3_client() -> boto3.client:
    """
    Creates and returns an S3 client using Boto3.

    Returns:
        boto3.client: The S3 client.
    """
    return boto3.client('s3')

def describe_instances(client: boto3.client) -> list:
    """
    Describes EC2 instances and returns a list of instances.

    Args:
        client (boto3.client): The EC2 client used to describe instances.

    Returns:
        list: A list of instances.
    """
    response = client.describe_instances()  # Call the describe_instances method to get information about EC2 instances
    instances = []
    for reservation in response['Reservations']:  # Iterate over each reservation in the response
        instances.extend(reservation['Instances'])  # Extend the instances list with instances from the reservation
    return instances

def create_ubuntu_instance(client: boto3.client) -> None:
    """
    Creates an Ubuntu EC2 instance.

    Args:
        client (boto3.client): The EC2 client used to create the instance.

    Returns:
        None
    """
    create_instance(client, "ami-04b70fa74e45c3917")  # Call create_instance with the Ubuntu AMI ID

def create_amazon_linux_2023_instance(client: boto3.client) -> None:
    """
    Creates an Amazon Linux 2023 EC2 instance.

    Args:
        client (boto3.client): The EC2 client used to create the instance.

    Returns:
        None
    """
    create_instance(client, "ami-08a0d1e16fc3f61ea")  # Call create_instance with the Amazon Linux 2023 AMI ID

def create_amazon_linux_2_instance(client: boto3.client) -> None:
    """
    Creates an Amazon Linux 2 EC2 instance.

    Args:
        client (boto3.client): The EC2 client used to create the instance.

    Returns:
        None
    """
    create_instance(client, "ami-0eaf7c3456e7b5b68")  # Call create_instance with the Amazon Linux 2 AMI ID

def create_instance(client: boto3.client, ami: str) -> None:
    """
    Creates an EC2 instance with the specified AMI.

    Args:
        client (boto3.client): The EC2 client used to create the instance.
        ami (str): The AMI ID to use for the instance.

    Returns:
        None
    """
    keyName = 'private-ec2'  # Key pair name for the instance
    client.run_instances(MaxCount=1,
                         MinCount=1,
                         ImageId=ami,
                         InstanceType="t2.micro",
                         KeyName=keyName,
                         SecurityGroupIds=['sg-0197b8159a5d886f8'])  # Run the instance with specified parameters

def list_buckets(s3_client: boto3.client) -> list:
    """
    Lists the names of all S3 buckets.

    Args:
        s3_client (boto3.client): The S3 client used to list buckets.

    Returns:
        list: A list of bucket names.
    """
    response = s3_client.list_buckets()  # Call the list_buckets method to get information about S3 buckets
    return [bucket['Name'] for bucket in response['Buckets']]  # Extract and return the list of bucket names

if __name__ == '__main__':
    ec2_client = get_ec2_client()  # Get the EC2 client
    # Uncomment the lines below to create instances
    #create_ubuntu_instance(ec2_client)
    #create_amazon_linux_2023_instance(ec2_client)
    #create_amazon_linux_2_instance(ec2_client)

    s3_client = get_s3_client()  # Get the S3 client
    response = s3_client.list_buckets()  # List the S3 buckets

    print(response)  # Print the response containing bucket information
