
# from __future__ import annotations  # 在文件顶部添加

from pydantic import BaseModel
from typing import Optional
from common.ModelRegistry import ModelRegistry


# 创建用户模型
@ModelRegistry.register
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

@ModelRegistry.register
class UserInfo(BaseModel):
    cid: Optional[str]= None
    
    class Config:
        from_attributes = True  # 允许从 ORM 对象转换
@ModelRegistry.register
class Order(BaseModel):
    id: int
    name: str
    # user: User
    class Config:
        from_attributes = True  # 允许从 ORM 对象转换

class UserResponse(BaseModel):
    id: int
    username: str
    password: str 


# 更新 class 之间的引用
# User.model_rebuild()
# Order.model_rebuild()
# UserInfo.model_rebuild()

# 一次性重建所有
ModelRegistry.rebuild_all()
