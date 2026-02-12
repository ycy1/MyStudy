import time
import  asyncio
import os
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有安装python-dotenv，则跳过加载
    pass

## 最新工厂构造模式
## Qwen/Qwen2.5-Coder-32B-Instruct
# model = init_chat_model(
#     model_provider="openai",
#     model="Qwen/Qwen2.5-72B-Instruct",
#     api_key=os.getenv("MODELSCOPE_API_KEY"),
#     base_url="https://api-inference.modelscope.cn/v1/",
#     temperature=0.7,
#     timeout=120,
#     max_tokens=1000,
# )

model = ChatOpenAI(
    api_key=os.getenv("MODELSCOPE_API_KEY"),
    base_url="https://api-inference.modelscope.cn/v1/",
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    max_tokens=200,
)

# model_ollama = ChatOllama(
#     model="deepseek-r1:1.5b",
#     temperature=0.7,
#     timeout=120,
#     max_tokens=100,
# )

# 
model_ollama = ChatOllama(
    model="deepseek-r1",
    model_kwargs={
        "function_calling": True,
        # "functions": functions  # 或在这里传入functions
    },  
    # temperature=0.7,
    # timeout=120,
    # max_tokens=2000,
    # other params...
)

# model_ollama = init_chat_model(
#     model_provider="ollama",
#     model="deepseek-r1:1.5b",
#     # api_key=os.getenv("MODELSCOPE_API_KEY"),
#     # base_url="https://api-inference.modelscope.cn/v1/",
#     temperature=0.7,
#     timeout=120,
#     max_tokens=100,
# )


prompt = ChatPromptTemplate.from_messages([
    ("system", f"""你一个专业的问答机器人:
    请使用XML标签，必须按如下格式输出：
    <thinks>你的思考过程<thinks/>
    <answer>你的最终答案<answer/>
    1.把思考过程放到<thinks><thinks/>标签里，最终答案放到<answer><answer/>标签里,保证标签闭合
    2.请使用<thinks><thinks/>标签来描述你的思考过程，请使用<answer><answer/>标签来描述你的答案。
    !! 必须按照以上输出，不能有额外的内容。
    
    
    """),
    
    ("human", "{query}"),
])

if __name__ == "__main__":
    # res = model_ollama.invoke(prompt.format(query="1+1=？ 把思考过程放到<thinks/>标签里"))
    for chunk in model_ollama.stream(prompt.format(query="周星驰的电影有哪些？")):   
        print(chunk.content, end="", flush=True)