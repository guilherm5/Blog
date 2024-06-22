import psycopg2
import os
from fastapi import HTTPException

def connect_database():
    print('Tentando estabelecer conexão com o banco de dados...')
    conn = None
    try:
        conn = psycopg2.connect(
            database=os.environ['database'],
            host=os.environ['host'],
            user=os.environ['usuario'],
            password=os.environ['senha']
        )
        print("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except psycopg2.Error as e:
        print(f'Erro ao realizar conexão com banco de dados, erro: {e}')
        raise HTTPException(status_code=500, detail=f'Erro ao realizar conexão com banco de dados, erro: {e}')
    