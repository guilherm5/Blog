from fastapi import APIRouter
from models.models import Usuario
from controllers.crud_usuario import create_user

router = APIRouter()

@router.post("/create-user")
async def post_new_user(user: Usuario):
    return await create_user(user)