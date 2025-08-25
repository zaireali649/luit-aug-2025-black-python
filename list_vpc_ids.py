import boto3  # AWS SDK for Python; used here to interact with AWS services

# Create an EC2 client to manage VPCs and other EC2-related resources
vpc_client = boto3.client('ec2')

# Call the describe_vpcs() method to retrieve details of all VPCs in the account
response = vpc_client.describe_vpcs()

# Extract the list of VPC objects from the response
vpcs = response['Vpcs']

# Iterate through each VPC object and print only the VPC ID
for vpc in vpcs:
    print(vpc['VpcId'])
