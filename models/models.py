from pydantic import BaseModel 
import bcrypt



class Usuario(BaseModel):
    nome_usuario: str | None = None
    email_usuario: str | None = None
    senha_usuario: str | None = None
    foto_usuario: str | None = None
    bio_usuario: str | None = None


    @staticmethod
    def encript_nome(password):
        password = password.encode(encoding="utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
        return hashed