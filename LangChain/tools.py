from langchain.tools import tool
from langchain_core.tools import StructuredTool


from model import model,model_ollama

@tool
def abc(a: int, b: int) -> int:
    """输入两个整数，返回两个整数的和."""
    return a + b  

# print(abc.args)
# print(abc.run({"a":1,"b":2}))
# res = abc.invoke({"a":1,"b":2})

def query (query: str) -> str:
    """输入一个查询，返回一个答案."""
    return query

## return_direct 决定工具的输出是否直接返回给用户，还是经过LLM的进一步处理。
query_tool = StructuredTool.from_function(query,return_direct=True)
print(abc)
# print(query_tool.invoke("你好,haha!"))

from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_community.tools import MoveFileTool
tools = [abc,MoveFileTool()]
tool_dict = {tool.name: tool for tool in tools}
def use_tool(tool_name: str, args: dict) -> str:
    """输入一个工具名和参数，返回工具的调用结果."""
    if tool_name in tool_dict:
        return tool_dict[tool_name].invoke(args)    
    else:
        return f"工具 {tool_name} 不存在"



# 4.这里需要将工具转换为openai函数，后续再将函数传入模型调用
# functions = [convert_to_openai_function(t) for t in tools]
# print(functions)
from langchain_core.messages import HumanMessage,SystemMessage
messages = [
    SystemMessage(content="你是一个专业的助手,你可以使用工具来解决问题."),
    HumanMessage(content="2+6=?"),
]   

mo2 = model.bind_tools(tools) ## 返回bind_tools后的模型，
# 必须使用bind_tools后的模型调用才可以调用到自定义的tool，使用的工具会在tool_calls中显示
res = mo2.invoke(messages)   
print(res)

# 处理工具调用
if hasattr(res, 'tool_calls') and res.tool_calls:
    for tool_call in res.tool_calls:
        print(f"工具调用: {tool_call}", type(tool_call['args']))
        result = use_tool(tool_call['name'], tool_call['args'])  
        print(f"工具调用结果: {result}")
else:
    print(f"模型响应: {res.content}")
