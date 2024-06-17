from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import requests
from jose import jwt
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GOOGLE_REDIRECT_URI = ""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@app.get("/auth/google")
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

@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])