from fastapi import APIRouter
from models.models import Usuario
from controllers.crud_usuario import create_user, get_users

app = APIRouter()   

@app.post("/create-user")
def post_new_user(user: Usuario):
    return create_user(user)

@app.get("/get-users")
def get_all_users():
    return create_user(get_users)