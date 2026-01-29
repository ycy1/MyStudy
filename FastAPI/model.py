
from pydantic import BaseModel
from typing import Optional

# 创建用户模型
class User(BaseModel):
    id: int
    username: str
    password: str 
    email: Optional[str] 
    is_active : bool
    is_superuser : bool
    address : Optional[str]
    nickname : Optional[str] = None
    info : Optional[UserInfo] = None
    orders :Optional[list[Order]] = []

class UserInfo(BaseModel):
    cid: Optional[str]= None


class Order(BaseModel):
    id: int
    name: str
    # user: User

class UserResponse(BaseModel):
    id: int
    username: str
    password: str 
