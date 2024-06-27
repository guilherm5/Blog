import boto3, botocore
from dotenv import load_dotenv
import os

load_dotenv()
# Credenciais da AWS e a região
aws_access_key_id = os.getenv('access_key_s3')
aws_secret_access_key = os.getenv('secret_key_s3')
region_name = os.getenv('region_name')

def connect_s3_service():
    try:
        s3 = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name
            )
        return s3 
    except botocore.exceptions.ClientError as error:
        return {"mensagem": "erro ao realizar conexão com s3 bucket"}
    finally:
        pass # Estudar close
        # Estudar __init__ 