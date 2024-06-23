from fastapi import APIRouter, Request, Depends
from models.model_usuario import Usuario
from controllers.crud_usuario import create_user, get_my_user, delete_user, update_user
from controllers.security import login_user, get_current_user

router_v1 = APIRouter(prefix="/v1", tags=["v2"])   
router_v2 = APIRouter(prefix="/v2", tags=["v2"], dependencies = [Depends(get_current_user)])

# Rotas - CRUD
@router_v1.post("/create-user")
def post_new_user(user: Usuario):
    return create_user(user)

@router_v2.get("/get-users")
def get_user(request: Request):
    return get_my_user(request)

@router_v2.delete("/delete-user")
def user_delete(user: Usuario, request: Request):
    return delete_user(user, request)

@router_v2.put("/update-user")
def put_user(user: Usuario, request: Request):
    return update_user(user, request)

# Rota - LOGIN 
@router_v1.post("/login-user")
def login(user: Usuario):
    return login_user(user)