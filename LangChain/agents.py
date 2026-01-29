from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import StructuredTool,Tool
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate,MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent, create_react_agent
from langchain_classic.agents import initialize_agent, AgentType
# from langchain_classic.agents import create_openai_functions_agent, AgentExecutor
from langchain_experimental.utilities import PythonREPL

from model import model,model_ollama

from pydantic import Field, BaseModel

class AddInput(BaseModel):
    a: int = Field(description="第一个整数")
    b: int = Field(description="第二个整数")
from typing import Union, Any

def abc(a: int, b: int) -> int:     
    """
      输入两个整数，返回它们的和
    """
    return a + b 

def abc2(params: dict|str) -> int:     
    """
      输入两个整数，返回它们的和
    """
    if isinstance(params, str):
        params = eval(params)

    return params["a"] + params["b"]

## 工具函数的入参提示明确
@tool
def abc3(params: dict|str) -> int:     
    """
      输入两个整数，返回它们的和，入参为一个字典或字符串，返回一个整数
      Args:
        params: 一个字典或字符串，包含两个整数a和b
        
      Returns:
        int: a和b的和
    """
    print("use_tool_params:",params,type(params))
    try:
        if isinstance(params, str):
            params = eval(params)
        return params["a"] + params["b"]
    except Exception as e:
        print(e)
        return 0
    


abc_tool = StructuredTool.from_function(
    func=abc,
    name="abc",
    description="用于计算两个整数的和，入参为两个整数，返回它们的和" 
)

abc_tool2 = StructuredTool.from_function(
    func=abc2,
    name="abc2",
    description="用于计算两个整数的和，入参为两个整数如果是字符串，则将其解析为字典，然后计算字典中a和b键对应的值的和，返回它们的和"    
)
# abc_tool = Tool(func=abc, name="abc",description="用于计算两个整数的和,入参为两个整数，返回一个整数",args=[int,int],return_direct=True)    
# abc_tool = StructuredTool.from_function(func=abc, name="abc",description="用于计算两个整数的和,入参为两个整数，返回一个整数")

# 创建一个包装函数来避免类型提示问题
# def search_wrapper(query: str) -> str:
#     """用于搜索互联网"""
#     return search.run(query)
# query_tool = StructuredTool.from_function(func=search_wrapper, name="search",description="用于搜索互联网")
# query_tool = Tool(func=search.run, name="search",description="用于搜索互联网")

# python_repl = PythonREPL() 
# calc_tool = Tool(func=PythonREPL().run, name="calc",description="用于计算，输入一个python表达式，返回表达式的结果")
# agent_executor = initialize_agent(
#     tools=[query_tool,calc_tool],
#     llm=model,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )
# tools = [abc_tool,calc_tool]
# tool_names = [tool.name for tool in tools]
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的助手,你可以使用工具来解决问题.当使用工具时，请提供正确的参数格式."),    
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

## 直接调用工具
# agent = create_tool_calling_agent(model, [abc3], prompt)
# agent_executor = AgentExecutor(agent=agent, tools=[abc3], verbose=True,handle_parsing_errors=True)
# res = agent_executor.invoke({"input": "计算10 与 20 的和"})  
# print(res)
from langchain_community.tools import MoveFileTool
search = TavilySearchResults(max_results=3)

tools = [abc3, MoveFileTool(),search]
from langsmith import Client
client = Client()
prompt = client.pull_prompt("hwchase17/react-chat")
## 模型会先思考，然后调用工具
agent = create_react_agent(model, tools, prompt)

from langchain_classic.memory.buffer import ConversationBufferMemory  # 或者从其他正确的位置导入
from langchain_classic.memory import ConversationSummaryBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.save_context({"input": "我叫张三"}, {"output": "好的"})

# history = ChatMessageHistory()
# history.add_user_message("你好呀!")
# history.add_ai_message("你好! 我是一个专业的问答机器人，你可以向我咨询任何问题。") 
## 超过指定token数，会自动总结之前的对话
memory3 = ConversationSummaryBufferMemory(llm=model_ollama,memory_key="chat_history",max_token_limit=200,return_messages=True) 
memory3.save_context({"input": "我叫张三"}, {"output": "好的"})


agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory3, verbose=True,handle_parsing_errors=True)
res = agent_executor.invoke({"input": "必须使用工具完成这个计算，查询北京的天气？"})    
print(res)

res = agent_executor.invoke({"input": "上海呢？"})  
print(res)

