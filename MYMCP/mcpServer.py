
'''
mcp协议的基本组成
{
  "jsonrpc": "2.0",
  "id": "string | number",
  "method": "string",
  "params": {
    "[key: string]": "unknown"
  }
}
jsonrpc：协议版本，固定为"2.0"。
id：请求的唯一标识符，可以是字符串或数字。
method：要调用的方法名称，是一个字符串。
params：方法的参数，是一个可选的键值对对象，其中键是字符串，值可以是任意类型。
'''

from typing import Any, Dict, List
from bilibili_api import search, sync
from mcp.server.fastmcp import FastMCP
import asyncio
import os
import requests
from openai import OpenAI
import mysql.connector
from mysql.connector import Error
import logging

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有安装python-dotenv，则跳过加载
    pass

# Configure logging to help with debugging MCP initialization issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Creating FastMCP server instance...")
mcp = FastMCP(
    name="MCP-Server",
    instructions="A Bilibili search and database management tool server for Bilibili search and database operations."
)

logger.info("MCP服务器实例已创建，名称为 'MCP-Server'")
logger.info("注意：MCP客户端必须先发送 'initialize' 请求，然后发送 'notifications/initialized'，再发送其他请求")
logger.info('请先发送初始化请求：{"method":"notifications/initialized","jsonrpc":"2.0"}')

# 输入: {"method":"notifications/initialized","jsonrpc":"2.0"}
# 输入: {"method":"tools/list","jsonrpc":"2.0","id":1}

@mcp.tool()
def blbl(keyword: str) -> dict[Any, Any]:
    """
    B站搜索工具
    """
    data = sync(search.search(keyword))
    return data


@mcp.tool()
def modelscope_chat_completion(
        prompt: str,
        model: str = "Qwen/Qwen2-7B-Instruct",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
    """
    调用ModelScope聊天完成API (使用OpenAI兼容接口)
    注意：需要设置MODELSCOPE_API_KEY环境变量
    API地址: https://api-inference.modelscope.cn/v1/
    """
    api_key = os.getenv("MODELSCOPE_API_KEY")
    if not api_key:
        return {"error": "MODELSCOPE_API_KEY环境变量未设置"}
    
    # ModelScope API需要特定的模型ID格式，通常与HuggingFace格式相同
    # 根据ModelScope API文档，使用原始模型ID格式
    # 但可能需要处理某些模型名称的映射
    model_mapping = {
        "Qwen/Qwen2-7B-Instruct": "Qwen/Qwen2-7B-Instruct",  # 保持原始格式
        "qwen2-7b-instruct": "Qwen/Qwen2-7B-Instruct",       # 映射到标准格式
        "Qwen/Qwen2.5-Coder-32B-Instruct": "Qwen/Qwen2.5-Coder-32B-Instruct",  # 您提供的示例
    }
    
    # 如果模型ID在映射中，则使用映射值，否则保持原样
    mapped_model = model_mapping.get(model, model)
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api-inference.modelscope.cn/v1/"
        )
        
        response = client.chat.completions.create(
            model=mapped_model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return {
            "model": response.model,
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0
            }
        }
    except Exception as e:
        return {"error": f"ModelScope API请求失败: {str(e)}"}

    
@mcp.tool()
def db_server(query: str) -> dict[Any, Any]:
    """
    Database server tool for executing SQL queries
    """
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "root"),
        "database": os.getenv("MYSQL_DATABASE", "fastapi_db")
    }
    
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            
            # Check if it's a SELECT query to return results
            if query.strip().upper().startswith('SELECT'):
                records = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                result = {
                    "columns": columns,
                    "rows": records,
                    "row_count": len(records),
                    "success": True
                }
            else:
                # For non-SELECT queries (INSERT, UPDATE, DELETE, CREATE, etc.)
                connection.commit()
                result = {
                    "message": f"Query executed successfully. Rows affected: {cursor.rowcount}",
                    "success": True
                }
            
            cursor.close()
            connection.close()
            return result
            
    except Error as e:
        return {"error": f"Database error: {str(e)}", "success": False}
    except Exception as e:
        return {"error": f"Error: {str(e)}", "success": False}


# async def test_blbl(keyword: str):
#     data = sync(search.search(keyword))
#     print(data)
#     return data


if __name__ == "__main__":
    mcp.run(transport='stdio')
