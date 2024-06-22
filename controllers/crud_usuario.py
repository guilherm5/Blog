import psycopg2 
from fastapi import HTTPException
from models.models import Usuario
from database.connect import connect_database
from fastapi import HTTPException 

conn = connect_database()

def create_user(user: Usuario):
    try:
        # Verifica se já existe usuário cadastrado
        cursor = conn.cursor()
        cursor.execute("SELECT u.email_usuario FROM usuario u WHERE email_usuario = %s", (user.email_usuario,))
        email_existing = cursor.fetchone()
        
        if email_existing:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        
        cursor.execute("INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) VALUES (%s, %s, %s)", 
                       (user.nome_usuario, user.email_usuario, user.encript_password(user.senha_usuario)))
        conn.commit()
        return {"mensagem": "sucesso"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()

def get_users():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()

        dict_users = []
        for row in usuarios:
            data = {
                "nome": row[1]
                , "email": row[2]
                , "bio": row[5]
                , "uuid_usuario": row[7]
            }
            dict_users.append(data)
        return dict_users
    except psycopg2.Error as e:
        return e  
    finally:
        cursor.close()

def delete_user(user: Usuario):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE uuid_usuario = %s", (str(user.uuid_usuario),))
        conn.commit()
        
        return {"message": "sucesso"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    finally:
        cursor.close()

def update_user(user: Usuario):
    try:
        cursor = conn.cursor()
        # Montando a tupla de parâmetros (o psycopg2 so aceita tuplas [linhas], então não posso passar os parametros 1 a 1)
        params = (
            user.nome_usuario,
            user.encript_password(user.senha_usuario),
            user.bio_usuario,
            str(user.uuid_usuario)
        )

        cursor.execute("""
            UPDATE usuario 
            SET nome_usuario = %s, senha_usuario = %s, bio_usuario = %s  
            WHERE uuid_usuario = %s
            """, params)
        conn.commit()
        
        return {"message": "sucesso"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()



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