"""
This is a simple agent of MCP Server
prompt: 提示词微调。
history: 模型上下文， 过多的历史会使模型回复速度过慢。
tools: 工具列表(MCP)。
query: 输入问题。

Usage:
    1. Install the required libraries by running `pip install -r requirements.txt`
    2. Run the script using `python mcpServer.py`
"""
from mcpServer import mcp as mcpServer
from openai import OpenAI
import asyncio
import os
from typing import Any, Dict, List
import json
from extract_json import get_formatted_json



# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有安装python-dotenv，则跳过加载
    pass

tools: List[Dict[str, Any]] = []
history: List[Dict[str, Any]] = []


async def chat_mode(query: str, history: list[dict[str, Any]]):
    print(f"history: {len(history)}")
    try:
        
        client = OpenAI(
            api_key= os.getenv("MODELSCOPE_API_KEY"),
            base_url="https://api-inference.modelscope.cn/v1/"
        )
        
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=history,
            temperature=0.3, # 模型温度
            top_p=0.5,
            max_tokens=5000,
            stream=False,
            timeout=200, # 超时时间
        )
        
        
        # 提取模型的回复
        model_reply = response.choices[0].message.content
        print(f"🎉模型回复：{model_reply}")
        # 尝试解析JSON，如果失败则返回None
        try:
            return json.loads(model_reply, strict=False)
        except json.JSONDecodeError as e:
            print(f"模型返回的内容不是有效的JSON格式: {e}")
            return json.loads(get_formatted_json(model_reply), strict=False)
    except Exception as e:
        print(f"Error: {e}")
        return None  # 在异常情况下也返回值


async def tool_use_fun(name: str, args: dict[str, Any]):
    print(f"🎉Tool use function: {name}")
    result = await mcpServer.call_tool(name, args)
    # print(f"🎉Tool回复：{result}")
    ## 只返回工具执行结果message 减少history长度
    result_content = result[1]["result"]["data"] if "data" in result[1]["result"] else result[1]["result"]["message"]
    
    print(f"🎉Tool回复：{result_content}")
    return str(result_content)

async def tool_get_fun():
    print("🎉Tool get function")
    result = await mcpServer.list_tools()
    for tool in result:
       tools.append({"name": tool.name, "description": tool.description, "inputSchema": tool.inputSchema})
    
    # print(tools)
    return tools

def prompt_fun(prompt: str):
    print("Prompt function")



# async def main():
#     print("Hello from myagent!")
#     query = "搜索关于Python的视频"
#     history.append({"role": "user", "content": query})
#     chat_mode(query, history)
#     tool_get_fun(query)


async def write_file (content: str, filename: str):
    with open(filename, "a", encoding="utf-8") as f:
        # f.write(json.dumps(content, ensure_ascii=False))
        f.write(content)
        f.write("\n")
        f.flush()
        print(f"Wrote {filename}")



if __name__ == "__main__":

    import time
    startTime = time.time()
    result = asyncio.run(tool_get_fun())
    print(result)
    # asyncio.run(tool_use_fun("blbl", {"keyword": "Python"}))
    
    json_format = json.dumps({
        "tool": "需要使用的工具名",
        "args": {
            "参数名": "参数值"
        },
        "message": "你的回答"
    }, ensure_ascii=False)
    prompt = f"""你是一个智能助手，你可以调用工具来完成任务。 
            重要规则：
            1. 当任务已完成或无法继续使用工具时，tool 字段应为空，不要继续循环使用工具
            2. 仅在确实需要工具来完成任务时才使用工具，一次只调用一个工具
            3. 如果工具返回结果表明任务已完成，请停止使用工具并提供最终答案
            5. 严格要求返回结果为JSON格式，使用双引号，且必须包含一个名为 "message" 的字段，该字段包含任务结果。
            6. 使用到数据库时如果表存在先读取原表结构使用原先结构不要修改原结构，不存在则创建表。
            7. 执行多条sql时，每条sql之间用分号隔开，超过五条时分批次执行，每次执行五条sql。
            8. 需要进行文件写入操作时，执行完检查文件是否写入成功。
            
            你可以调用的工具列表如下，请使用以下工具来帮助完成我的任务：
            {tools};
            
            重点：只能返回一个json对象，不要返回数组，一次只调用一个工具，不要同时调用多个工具
            重点：回答完成后，你的返回的格式必须如下（严格要求返回结果为JSON格式，且必须包含一个名为 "message" 的字段，该字段包含任务结果.
            以下是一个例子：
            {json_format}
            
            
    """
    
    query = """
    1.搜索关于Python的视频，2.连接db_server 数据库 创建并写入ai_blbl表中 ai_blbl包括视频id、视频标题、视频描述(注:取一句话即可)、视频url、视频发布时间(时间戳)
    如果表存在则先读取原表结构使用原先结构不要修改原结构3.把所有的入表sql语句写入output.sql文件中
    """

    history.insert(0, {"role": "system", "content": prompt})
    history.insert(1, {"role": "user", "content": query})
    flag = True
    while flag:
        # if len(history) > 10:
        #     history = history[:10]  ## 保留最新的10条记录
        #     history.insert(0, {"role": "system", "content": prompt})
        #     history.insert(1, {"role": "user", "content": query})
           
        agentRes = asyncio.run(chat_mode(query, history))
        print(f"🎉模型回复2：{agentRes}")
        # Convert agentRes to string if it's a dict, otherwise use as is
        ## if isinstance(agentRes, dict) and agentRes["message"] else agentRes
        content_str = str(agentRes) 
        history.append({"role": "assistant", "content": content_str})
        
        # print(f"🎉模型回复3：{isinstance(agentRes, list)} {len(agentRes)}")
        if isinstance(agentRes, list) and len(agentRes) > 0:
            for item in agentRes:
                # 检查agentRes是否为字典类型且包含tool字段
                if item and isinstance(item, dict) and "tool" in item and item["tool"]:
                    tool_result = asyncio.run(tool_use_fun(item["tool"], item["args"]))
                    # print(f"🎉Tool result：{tool_result}")
                    
                    # 将工具执行结果以更清晰的方式添加到历史记录中
                    # 添加一个用户消息来表示工具执行结果，这样模型能更好地理解上下文
                    tool_execution_message = f"工具 {item['tool']} 执行结果: {tool_result}"
                    history.append({"role": "assistant", "content": tool_execution_message})
                else:
                    print("No tool used")
                    flag = False ## 结束循环
                    endTime = time.time()
                    print(f"耗时：{endTime - startTime}")
        else:
            if agentRes and isinstance(agentRes, dict) and "tool" in agentRes and agentRes["tool"]:
                tool_result = asyncio.run(tool_use_fun(agentRes["tool"], agentRes["args"]))
                # print(f"🎉Tool result：{tool_result}")
                
                # 将工具执行结果以更清晰的方式添加到历史记录中
                # 添加一个用户消息来表示工具执行结果，这样模型能更好地理解上下文
                tool_execution_message = f"工具 {agentRes['tool']} 执行结果: {tool_result}"
                history.append({"role": "assistant", "content": tool_execution_message})
            else:
                print("No tool used")
                flag = False ## 结束循环
                endTime = time.time()
                print(f"耗时：{endTime - startTime}")