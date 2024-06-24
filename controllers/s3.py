import boto3

S3 = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''  
)

print(S3)
