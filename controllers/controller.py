from fastapi import APIRouter, HTTPException
from models.models import Usuario
from database.connect import connect_database

app = APIRouter()

@app.post("/create-user")
def create_user(user: Usuario):
    try:
        conn = connect_database()  
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) VALUES (%s, %s, %s)", (user.nome_usuario, user.email_usuario, user.encript_nome(user.senha_usuario)))
        conn.commit()  # Aplica a transação no banco de dados
        return {"message": "Usuário criado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao cadastrar usuário: {str(e)}")
    finally:
        cursor.close()
        conn.close()  

