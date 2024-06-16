from fastapi import FastAPI
from controllers.controller import app

router = FastAPI()

router.include_router(app)

