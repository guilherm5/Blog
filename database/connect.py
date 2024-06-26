import psycopg2
import os
from fastapi import HTTPException

# Estudar pool de conexão
def connect_database():
    print('Tentando estabelecer conexão com o banco de dados...')

    try:
        conn = psycopg2.connect(
            database = os.getenv('database'),
            host = os.getenv('host'),
            user = os.getenv('user'),
            password = os.getenv('senha'),
        )
        print("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except psycopg2.Error as e:
        print(f'Erro ao realizar conexão com banco de dados, erro: {e}')
        raise HTTPException(status_code=500, detail=f'Erro ao realizar conexão com banco de dados, erro: {e}')