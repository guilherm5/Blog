from fastapi import APIRouter
from models.models import Usuario
from controllers.crud_usuario import create_user

app = APIRouter()   

@app.post("/create-user")
def post_new_user(user: Usuario):
    return create_user(user)