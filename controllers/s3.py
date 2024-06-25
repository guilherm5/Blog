import boto3

# Configure suas credenciais da AWS e a região
aws_access_key_id = ''
aws_secret_access_key = ''
region_name = ''

# Nome do bucket
bucket_name = ''
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

imagens = get_images()
if imagens:
    first_image = imagens[0]
    key = first_image['Key']
    print(f"Nome do primeiro objeto: {key}")
else:
    print("Nenhuma imagem encontrada.")

