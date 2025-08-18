from helpers import * 

def create_instances(ec2_client, ami_type="Ubuntu", ami_amount=1):
    normalized_ami_type = ami_type.lower().strip().replace(" ", "")

    for i in range(ami_amount):
        if normalized_ami_type == "ubuntu":
            create_ubuntu_instance(ec2_client)
            print("Ubuntu Created")
        elif normalized_ami_type == "linux2023":
            create_amazon_linux_2023_instance(ec2_client)
            print("Linux 2023 Created")
        elif normalized_ami_type == "linux2":
            create_amazon_linux_2_instance(ec2_client)
            print("Linux 2 Created")
        else:
            print("Unsupported AMI")
    
if __name__=="__main__":
    ec2_client = get_ec2_client()
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