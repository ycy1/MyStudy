import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config.dbConfig import init_db,close_db
from reqApp import init_router
from contextlib import asynccontextmanager
from config.settings import settings
from common.Middleware import my_middleware
from config.redisCfg import redis_connect


@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    应用生命周期管理
    '''
    await init_db(app) # 初始化数据库
    print("启动数据库")
    redis_client = await redis_connect()
    app.state.redis = redis_client
    yield
    # 关闭时断开数据库连接
    await close_db()
    await app.state.redis.close()
    print("关闭数据库、关闭redis连接")

app = FastAPI(lifespan=lifespan, version=settings.app_version, title=settings.app_name)

app.mount("/static", StaticFiles(directory=settings.static_folder), name="static") # 挂载静态文件
init_router(app) # 初始化路由
# my_middleware(app)  ## 中间件

@app.get("/")
async def index():
    return {"message": "Hello World", "version": f"{settings.app_version}", "url": "/docs"}


if __name__ == "__main__":
    for route in app.routes:
        print(str(route)) ## 启动时输出所有路由
    uvicorn.run('main:app', host=settings.host, port=settings.port, reload=True)
