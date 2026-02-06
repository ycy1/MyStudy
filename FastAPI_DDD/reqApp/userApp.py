from fastapi import APIRouter
# from orm import User
from model import User

user_router = APIRouter(tags=['用户应用'], prefix='/user')


@user_router.post('/create')
async def create_user(user: User):
    user2 = await User.create(**user.model_dump())
    return user2



