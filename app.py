from fastapi import FastAPI
from routes.user import app

router = FastAPI()

router.include_router(app)