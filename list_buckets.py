import boto3  # AWS SDK for Python; used here to interact with AWS S3

# Create an S3 client using default credentials/configuration
s3 = boto3.client('s3')

# Call the list_buckets() method to retrieve all S3 buckets in the account
response = s3.list_buckets()

# Extract the list of bucket metadata from the response
buckets = response["Buckets"]

# Iterate through each bucket object and print only the bucket name
for bucket in buckets:
    print(bucket["Name"])
