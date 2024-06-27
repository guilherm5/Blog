from utils.connect_bucket import connect_s3_service
from dotenv import load_dotenv
import os

load_dotenv()
bucket_name = os.getenv('bucket_name')
def get_images():
    try:
        s3 = connect_s3_service()
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects_list = response['Contents']
        print(f"Objetos encontrados: {len(objects_list)}")  
        return objects_list
    except Exception as e:
        print('Erro ao buscar imagens:', e)
        return []


imagens = get_images()
if imagens:
    first_image = imagens[0]
    key = first_image['Key']
    print(f"Nome do primeiro objeto: {key}")
else:
    print("Nenhuma imagem encontrada.")
    
    
def upload_images():
    try:
        s3 = connect_s3_service()
        with open('maxresdefault (1).jpg', "rb") as f:
            s3.upload_fileobj(f, bucket_name, 'maxresdefault (1).jpg')
            print("Upload realizado com sucesso.")
    except Exception as e:
        print('Erro ao fazer upload da imagem:', e)

# Executando a função upload_images
#upload_images()