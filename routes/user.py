from fastapi import APIRouter
from models.model_usuario import Usuario
from controllers.crud_usuario import create_user, get_users, delete_user, update_user
from controllers.security import login_user
app = APIRouter()   

# Rotas - CRUD
@app.post("/create-user")
def post_new_user(user: Usuario):
    return create_user(user)

@app.get("/get-users")
def get_all_users():
    return get_users()

@app.delete("/delete-user")
def user_delete(user: Usuario):
    return delete_user(user)

@app.put("/update-user")
def user_update(user: Usuario):
    return update_user(user)

# Rota - LOGIN 
@app.post("/login-user")
def login(user: Usuario):
    return login_user(user)