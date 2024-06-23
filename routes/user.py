from fastapi import APIRouter, Request, Depends, HTTPException
from models.model_usuario import Usuario
from controllers.crud_usuario import create_user, get_users, delete_user, update_user
from controllers.security import login_user, get_current_user
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
def put_user(user: Usuario, request: Request, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Não autorizado")
    return update_user(user, request)

# Rota - LOGIN 
@app.post("/login-user")
def login(user: Usuario):
    return login_user(user)