import psycopg2
import os

def connect_database():
    try:
        conn = psycopg2.connect(
            database=os.environ['database'],
            host=os.environ['host'],
            user=os.environ['usuario'],
            password=os.environ['senha'],
            port=os.environ['port']
        )
        print("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except psycopg2.Error as e:
        print(f'Erro ao realizar conexão com banco de dados, erro: {e}')
        return f'Erro ao realizar conexão com banco de dados, erro: {e}'