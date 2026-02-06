'''
应用配置管理
'''
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


# python-dotenv

class Settings(BaseSettings):
    '''
    应用配置类
    '''
    # 应用配置
    app_name: str = "FastAPI DDD"
    app_version: str = "0.1.0"
    static_folder: str = "static"
    host: str = "127.0.0.1"
    port: int = 8000

    # debug: bool = True
    # secret_key: str = 'your-secret-key'

    # 数据库配置
    # db_url: str = "sqlite://./data/test.db"

    # class Config:
    #     '''
    #     数据库配置类
    #     '''
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()

if __name__ == "__main__":
    print(settings.app_name)
