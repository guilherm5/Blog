from datetime import datetime, timedelta
from jwt import DecodeError, decode, encode, ExpiredSignatureError
import pytz
import os
import psycopg2 
from fastapi import HTTPException, Request
from pydantic import ValidationError
from models.model_usuario import Usuario
from database.connect import connect_database
from dotenv import load_dotenv

load_dotenv()
conn = connect_database()
SECRET_KEY = os.getenv('secret_key')
ALGORITHM = os.getenv('algorithm')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('access_token_expire_minutes')

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(pytz.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login_user(user: Usuario):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT 
                    u.email_usuario
                    , u.senha_usuario 
                    , u.id_usuario 
                FROM usuario u 
                WHERE u.email_usuario = %s
            """, (user.email_usuario,)
        )
        email_existing = cursor.fetchone()

        # Verifica se existe conta
        if not email_existing:
            raise HTTPException(status_code=401, detail=f"O email [{user.email_usuario}] é inexistente. Por favor, realize seu cadastro.")
        # Verifica se a senha esta correta
        if not user.password_verify(user.senha_usuario, email_existing[1]):
            raise HTTPException(status_code=401, detail="Senha incorreta. Por favor, verifique-a e tente novamente.")

        access_token = create_access_token(data={
            'sub': email_existing[0],
            'id': email_existing[2]
        })
        return access_token 

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except (psycopg2.Error, Exception) as e:
        conn.rollback()  # Desfaz a transação pendente
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def get_current_user(request: Request):
    cursor = None
    authorization = request.headers.get('Authorization')
    if not authorization:
        raise HTTPException(status_code=400, detail="Erro ao enviar requisição, confira seus dados ou consulte o desenvolvedor do sistema.")
    
    token = authorization.split()[1]
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = {
            'sub': payload.get('sub'),
            'id': payload.get('id')
        }
        if not user:
            raise HTTPException(status_code=401, detail="Credenciais inválidas.")
        
        # Verifica se usuário existe no banco de dados
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                u.nome_usuario,
                u.email_usuario,
                u.bio_usuario,
                u.id_usuario,
                u.uuid_usuario
            FROM usuario u 
            WHERE u.email_usuario = %s
            """, (user['sub'],)
        )
        user_existing = cursor.fetchone()
        if not user_existing:
            raise HTTPException(status_code=401, detail="Usuário não encontrado na base de dados. Por favor, realize o cadastro.")
        elif user_existing[3] != user['id']:
            raise HTTPException(status_code=401, detail="O sistema encontrou inconsistência entre os dados de login e cadastro, impossível realizar autenticação.")
        
        request.state.my_attr = {
            "nome_usuario": user_existing[0],
            "email_usuario": user_existing[1],
            "bio_usuario": user_existing[2],
            "id_usuario": user_existing[3],
            "uuid_usuario": user_existing[4]
        }
        return request.state.my_attr
    
    except DecodeError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token de autenticação expirado. Por favor, realize o login novamente.")
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro inesperado ao realizar consulta de usuário. Erro: {e}")
    finally:
        if cursor:
            cursor.close()