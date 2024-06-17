from fastapi import APIRouter, HTTPException
from models.models import Usuario
from database.connect import connect_database

app = APIRouter()

@app.post("/create-user")
def create_user(user: Usuario):
    try:
        conn = connect_database()  
        cursor = conn.cursor()

        # verifica se ja existe usuario cadastrado
        cursor.execute("SELECT u.email_usuario FROM usuario u WHERE email_usuario = %s", (user.email_usuario,))
        email_existing = cursor.fetchone()
        
        if email_existing:
            raise HTTPException(status_code=400, detail="Email ja cadastrado.")     

        cursor.execute("INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) VALUES (%s, %s, %s)", (user.nome_usuario, user.email_usuario, user.encript_nome(user.senha_usuario)))

        conn.commit()  
        return {"mensagem": "sucesso"}
    except Exception as e:
        return e
    finally:
        cursor.close()
        conn.close()  

