from fastapi import FastAPI
from routes.user import router_v1, router_v2

router = FastAPI()

router.include_router(router_v1)
router.include_router(router_v2)