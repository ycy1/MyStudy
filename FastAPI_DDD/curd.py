
from orm import User, UserInfo, Order, Post, UserPost
from model import User as UserModel
from tortoise.expressions import Q
from common.ModelConverter import ModelConverter



async def list_user(keyword):
   
    if keyword:
        list = await User.filter(Q(username__icontains=keyword) | Q(nickname__icontains=keyword))
        # list = await User.filter(username__contains=keyword)
    else:
        list = await User.all()
    return list

async def query_user(id):
    user = await User.filter(id=id).first()
    return user

async def create_user(username, password) -> User:
    user = await User.create(username=username, password=password)
    return user

async def update_user(user_id, username, password) -> User:
    user = await User.get_or_none(id=user_id)
    if user:
        await User.filter(id=user_id).update(username=username, password=password)
    else:
        raise  Exception("用户不存在")
    return user

async def delete_user(user_id):
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
    else:
        raise  Exception("用户不存在")
    
async def test_create_user(username, password):
    info = await UserInfo.create(cid="123")
    user = await User.create(username=username, password=password,info=info)
    return user

async def test_create_user2(username, password):
    user = await User.create(username=username, password=password)
    order = await Order.create(name="订单1", user=user)
    order1 = await Order.create(name="订单2", user=user)
    order2 = await Order.create(name="订单3", user=user)
    return [order, order1, order2]

async def test_create_user3(username, password):
    user = await User.create(username=username, password=password)
    post = await Post.create(name="岗位web")
    post2 = await Post.create(name="岗位app")
    userpost = await UserPost.create(user=user, post=post)
    userpost2 = await UserPost.create(user=user, post=post2)
    return [post, post2]

async def test_update_user():
    user = await User.get(id=32)
    info = await UserInfo.create(cid="789")
    user.info = info
    await user.save()

    # await User.filter(id=32).update(info=info)
    return user

async def test_query_user():
    user = await User.get(id=30).prefetch_related("orders","info")
    usermodel = ModelConverter._orm_to_model(user, UserModel)
    return usermodel
async def test_query_user2():
    user = await User.get(id=30).prefetch_related("orders", "info")
    usermodel = ModelConverter._orm_to_model(user, UserModel)
    return usermodel

async def test_delete_user():
   user = await User.get(id=31)
   await user.delete()



# async def main():
#     user = await create_user("小明", "123")
#     print(f"创建用户：{user.username}")
#     user = await create_user("小李", "456")
#     print(f"创建用户：{user.username}")
#     user = await create_user("小王", "789")
#     print(f"创建用户：{user.username}")

#     # 正确关闭连接
#     await Tortoise.close_connections()


if __name__ == "__main__":
    print("curd")
    # asyncio.run(main())
    