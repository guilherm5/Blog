from datetime import datetime, timedelta
from jwt import encode
from pwdlib import PasswordHash
import pytz
import os
import psycopg2
from fastapi import HTTPException
from pydantic import ValidationError
from models.model_usuario import Usuario
from database.connect import connect_database

conn = connect_database()
pwd_context = PasswordHash.recommended()
SECRET_KEY = os.environ['secret_key']
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(pytz.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login_user(user: Usuario):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT 
                    u.id_usuario 
                    , u.senha_usuario 
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
            'sub': user.email_usuario,
            'id': email_existing[0]
        })
        return access_token 

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except (psycopg2.Error, Exception) as e:
        conn.rollback()  # Desfaz a transação pendente
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
