import boto3
from dotenv import load_dotenv
import os

load_dotenv()
# Credenciais da AWS e a região
aws_access_key_id = os.getenv('access_key_s3')
aws_secret_access_key = os.getenv('secret_key_s3')
region_name = os.getenv('region_name')
bucket_name = os.getenv('bucket_name')

def get_images():
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        response = s3.list_objects_v2(Bucket=bucket_name)
        objects_list = response['Contents']
        print(f"Objetos encontrados: {len(objects_list)}")  
        return objects_list
    except Exception as e:
        print('Erro ao buscar imagens:', e)
        return []


"""
TESTE GET IMAGENS
imagens = get_images()
if imagens:
    first_image = imagens[0]
    key = first_image['Key']
    print(f"Nome do primeiro objeto: {key}")
else:
    print("Nenhuma imagem encontrada.")
"""
    
    
def upload_images():
    s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
    )
    print(bucket_name)
    try:
        with open('maxresdefault (1).jpg', "rb") as f:
            s3.upload_fileobj(f, bucket_name, 'maxresdefault (1).jpg')
            print("Upload realizado com sucesso.")
    except Exception as e:
        print('Erro ao fazer upload da imagem:', e)

# Executando a função upload_images
upload_images()