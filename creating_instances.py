from helpers import * 
from typing import Any

def create_instances(ec2_client: Any, ami_type: str = "Ubuntu", ami_amount: int = 1) -> None:
    """
    Creates EC2 instances of a specified AMI type using the provided EC2 client.

    Args:
        ec2_client (Any): The boto3 EC2 client used to interact with AWS EC2.
        ami_type (str, optional): The type of AMI to launch. Supported values are
            "Ubuntu", "Linux2023", and "Linux2". Defaults to "Ubuntu".
        ami_amount (int, optional): The number of instances to create. Defaults to 1.

    Returns:
        None: This function does not return a value. It prints messages indicating the
        type of instance(s) created or an error message if the AMI type is unsupported.
    """
    # Normalize the AMI type (case-insensitive, no extra spaces)
    normalized_ami_type = ami_type.lower().strip().replace(" ", "")

    # Create the specified number of instances
    for i in range(ami_amount):
        if normalized_ami_type == "ubuntu":
            create_ubuntu_instance(ec2_client)  # Call helper function to create Ubuntu instance
            print("Ubuntu Created")
        elif normalized_ami_type == "linux2023":
            create_amazon_linux_2023_instance(ec2_client)  # Create Amazon Linux 2023 instance
            print("Linux 2023 Created")
        elif normalized_ami_type == "linux2":
            create_amazon_linux_2_instance(ec2_client)  # Create Amazon Linux 2 instance
            print("Linux 2 Created")
        else:
            print("Unsupported AMI")  # Handle unsupported AMI types
    
if __name__ == "__main__":
    # Get an EC2 client using a helper function
    ec2_client = get_ec2_client()
    
    # Example calls with different AMI types and amounts
    create_instances(ec2_client, "ubuNtu")
    create_instances(ec2_client, "  Linux 2")
    create_instances(ec2_client)
    create_instances(ec2_client, "Linux 2")
    create_instances(ec2_client, ami_type="Linux 2023")
    create_instances(ec2_client, ami_type="Linux  2023")
    create_instances(ec2_client, ami_type="Centos")
    create_instances(ec2_client, "Linux 2", 2)
    create_instances(ec2_client, "Linux 2", ami_amount=3)
    create_instances(ec2_client, ami_amount=5)
    create_instances(ec2_client, ami_amount=4, ami_type="Linux 2023")
