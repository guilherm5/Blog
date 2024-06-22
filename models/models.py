from pydantic import BaseModel, Field
from uuid import UUID, uuid4
import bcrypt



class Usuario(BaseModel):
    id_usuario: int | None = None
    uuid_usuario: UUID = Field(default_factory=uuid4)
    nome_usuario: str | None = None
    email_usuario: str | None = None
    senha_usuario: str | None = None
    foto_usuario: str | None = None
    bio_usuario: str | None = None

    @staticmethod
    def encript_password(password):
        password = password.encode(encoding="utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
        return hashed