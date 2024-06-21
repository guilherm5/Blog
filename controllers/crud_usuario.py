from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.models import Usuario
from database.connect import connect_database
from fastapi import HTTPException, Depends 

def create_user(user: Usuario):
    cursor = connect_database()
    try:
        # Verifica se já existe usuário cadastrado
        cursor.execute("SELECT u.email_usuario FROM usuario u WHERE email_usuario = %s", (user.email_usuario,))
        email_existing = cursor.fetchone()
        if email_existing:
            raise HTTPException(status_code=400, detail="Email já cadastrado.")
        
        cursor.execute("INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) VALUES (%s, %s, %s)", 
                       (user.nome_usuario, user.email_usuario, user.encript_nome(user.senha_usuario)))
        cursor.commit()
        return {"mensagem": "sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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