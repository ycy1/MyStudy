from fastapi.responses import Response
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from dbConfig import app  # 直接导入已经创建的应用实例

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
中间件
按注册顺序倒序执行
'''

@app.middleware("http")
async def middleware(request, call_next):
    print("中间件1 开始执行")
    response = await call_next(request)
    print("中间件1 结束执行")
    return response

@app.middleware("http")
async def middleware2(request, call_next):
    print("中间件2 开始执行")
    response = await call_next(request)
    print("中间件2 结束执行")
    return response


# class TestMiddleware:
#     def __init__(self, app):
#         self.app = app

#     async def __call__(self, scope, receive, send):
#         print("中间件3 运行")
#         response = await self.app(scope, receive, send)
#         print("中间件3 结束")

# app.add_middleware(TestMiddleware)