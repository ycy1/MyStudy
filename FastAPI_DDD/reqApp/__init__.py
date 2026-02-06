from fastapi import APIRouter
from .userApp import user_router
# from .item import item_router

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(user_router)
# v1_router.include_router(item_router)



def init_router(app: FastAPI):
    app.include_router(v1_router)
