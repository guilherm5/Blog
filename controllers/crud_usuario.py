import psycopg2
from fastapi import HTTPException, Request
from pydantic import ValidationError
from models.model_usuario import Usuario
from database.connect import connect_database
from utils.connect_bucket import connect_s3_service
from dotenv import load_dotenv
import os

conn = connect_database()
bucket_name = os.getenv('bucket_name')

def create_user(user: Usuario):
    try:
        cursor = conn.cursor()
        # Verifica se já existe usuário cadastrado
        cursor.execute(
            """
                SELECT 
                    u.email_usuario 
                FROM usuario u 
                WHERE email_usuario = %s
            """, (user.email_usuario,)
        )
        email_existing = cursor.fetchone()
        if email_existing:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        
        # Se não existir, insere
        cursor.execute(
            """
                INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) 
                VALUES (%s, %s, %s)
            """, (user.filtro_nome(user.nome_usuario), user.email_usuario, user.password_hash(user.senha_usuario))
        )
        conn.commit()

        return {"mensagem": "sucesso"}
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except (psycopg2.Error, Exception) as e:
        conn.rollback()  # Desfaz a transação pendente
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def get_my_user(request: Request):
    cursor = None 
    try:
        uuid_usuario = request.state.my_attr['uuid_usuario']
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE uuid_usuario = %s", (uuid_usuario,))
        usuario = cursor.fetchone()
        
        return {
            'id_usuario': usuario[0], 
            'nome_usuario': usuario[1],
            'foto_usuario': usuario[4],
            'bio_usuario': usuario[5], 
            'data_cadastro_usuario': usuario[6],
            'uuid_usuario': usuario[7]
        }
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def delete_user(user: Usuario, request: Request):
    cursor = None
    try:
        uuid_usuario = request.state.my_attr['uuid_usuario']
        if uuid_usuario != str(user.uuid_usuario):
            raise HTTPException(status_code=400, detail="Você não tem permissão para deletar este usuário.")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE uuid_usuario = %s", (str(user.uuid_usuario),))
        conn.commit()
        
        return {"message": "sucesso"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor: 
            cursor.close()

def update_user(user: Usuario, request: Request):
    cursor = None
    try:
        uuid_usuario = request.state.my_attr['uuid_usuario']
        if uuid_usuario != str(user.uuid_usuario):
            raise HTTPException(status_code=400, detail="Você não tem permissão para alterar este usuário.")
        
        cursor = conn.cursor()
        params = (
            user.nome_usuario,
            user.password_hash(user.senha_usuario),
            user.bio_usuario,
            str(user.uuid_usuario)
        )

        cursor.execute("""
            UPDATE usuario 
            SET nome_usuario = %s, senha_usuario = %s, bio_usuario = %s  
            WHERE uuid_usuario = %s
            """, params)
        conn.commit()
        
        return {"message": "Usuário atualizado com sucesso"}
    
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if cursor:
            cursor.close()

def get_image_s3():
    try:
        s3 = connect_s3_service()
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects_list = response['Contents']
        print(f"Objetos encontrados: {len(objects_list)}")  
        return objects_list
    except Exception as e:
        print('Erro ao buscar imagens:', e)
        return []

"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GOOGLE_REDIRECT_URI = ""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print(access_token)
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])
"""