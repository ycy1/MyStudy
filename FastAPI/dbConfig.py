import os
from typing import Dict, Any
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# @app.get("/list_user")
# async def list_user():
#  return {"user":"66"}

# 数据库配置项，可通过环境变量覆盖
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

# Tortoise ORM 配置
TORTOISE_ORM_CONFIG: Dict[str, Any] = {
    "connections": {
        # 默认使用 SQLite，可通过环境变量配置其他数据库
        "default": 'mysql://root:root@localhost:3306/fastapi_db'
    },
    "apps": {
        "models": {
            "models": [
                "orm",  # 你的模型文件所在模块
                "aerich.models"  # Aerich 迁移工具需要的模型
            ],
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 是否使用时区
    "timezone": "Asia/Shanghai",  # 设置时区
    "db_pool": {
        "min_size": 1,  # 连接池最小连接数
        "max_size": 10, # 连接池最大连接数
        "timeout": 30,  # 连接超时时间（秒）
        "max_lifetime": 3600,  # 连接最大生命周期（秒）
        "idle_timeout": 30,  # 连接空闲超时时间（秒）
    },
}


# def init_db(app):
#     # 数据库连接
#     register_tortoise(
#         app,
#         config=TORTOISE_ORM_CONFIG,
#         generate_schemas=True,  # 自动生成数据库表
#         add_exception_handlers=True,  # 自动添加异常处理
#     )
#     print("数据库连接成功")



# 不同数据库的配置示例（可根据需要启用）
DB_CONFIGS = {
    "sqlite": {
        "connections": {"default": "sqlite://db.sqlite3"},
        "apps": {
            "models": {
                "models": ["models", "aerich.models"],
                "default_connection": "default",
            }
        }
    },
    "mysql": {
        "connections": {
            "default": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": os.getenv("MYSQL_HOST", "localhost"),
                    "port": int(os.getenv("MYSQL_PORT", 3306)),
                    "user": os.getenv("MYSQL_USER", "root"),
                    "password": os.getenv("MYSQL_PASSWORD", ""),
                    "database": os.getenv("MYSQL_DATABASE", "test"),
                }
            }
        }
    }
}

# 数据库连接
register_tortoise(
    app,
    config=TORTOISE_ORM_CONFIG,
    generate_schemas=True,  # 自动生成数据库表
    add_exception_handlers=True,  # 自动添加异常处理
)

import reqApp  ## 路由
import middleware ## 中间件


if __name__ == "__main__":
    for route in app.routes:
        print(str(route)) ## 启动时输出所有路由
    uvicorn.run('dbConfig:app', host="127.0.0.1", port=8022, reload=True)
    
