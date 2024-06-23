from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from pwdlib import PasswordHash
import random

pwd_context = PasswordHash.recommended()

# Estudar jeito de filtrar campos ou criar classes separadas (quero que todos alguns campos sejam obrigatorios.).
# Atualmente, se eu enviar um json sem chaves ele vai inserir no meu banco. Buscar soluções.
class Usuario(BaseModel):
    id_usuario: int | None = None
    uuid_usuario: UUID = Field(default_factory=uuid4)
    nome_usuario: Optional[str] = None
    email_usuario: str | None = None 
    senha_usuario: str | None = None 
    foto_usuario: str | None = None
    bio_usuario: str | None = None
    
    @staticmethod
    def filtro_nome(nome: str) -> str:
        if nome == "" or nome == None: 
            nome = f'usuario_{random.randint(1, 1000)}'
        return(nome)

    @staticmethod
    def password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def password_verify(plain_password: str, hashed_password: str) -> str:
        return pwd_context.verify(plain_password, hashed_password)
    
class Token(BaseModel):
    access_token: str
    token_type: str