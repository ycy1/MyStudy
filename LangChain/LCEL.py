"""
LCEL（LangChain Expression Language）是一种声明式语言，用于：
构建复杂的链
组合不同的组件
处理输入输出
添加中间步骤和转换

链式调用 管道符分割 按顺序传递返回，传参为首位对象的入参
每个对象都实现了Runnable接口，都有invoke方法
"""

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser,XMLOutputParser,CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_classic.chains.llm import LLMChain
from langchain_classic.chains.sequential import SimpleSequentialChain,SequentialChain
from langchain_classic.chains.sql_database.query import create_sql_query_chain

from model import model,model_ollama
from db import db

def read_file():
    with open("test.txt", "r", encoding="utf-8") as f:
        content = f.read()  
        print(content)
        return content

## 每个解析器都有 get_format_instructions函数
json_parser = JsonOutputParser()
xml_parser = XMLOutputParser()
list_parser = CommaSeparatedListOutputParser()

# print(list_parser.get_format_instructions())
chat_promptdb = ChatPromptTemplate.from_messages([
    ("system", f"你是一个专业的问答机器人，使用{list_parser.get_format_instructions()}格式的回答"),
    ("human", "{query}"),
])
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", f"你是一个专业的问答机器人，使用{list_parser.get_format_instructions()}格式的回答"),
    ("human", "{data}"),
    ("human", "{query}"),
])
format = json_parser.get_format_instructions()
chat_prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个{post}，请使用"+format+"格式的回答"), 
    ("human", "{data}"),
    ("human", "{query2}"),
])


## 链式调用 管道符分割 按顺序传递返回,传参为首位对象的入参
# chain = chat_prompt | model | json_parser 
# print(chain.invoke({"query": f"你好,{json_parser.get_format_instructions()}"}))

# chain = chat_prompt | model | xml_parser 
# print(chain.invoke({"query": f"你好,请输出周星驰的电影"}))

# chain = chat_prompt | model | list_parser
# print(chain.invoke({"query": f"你好,请输出周星驰的电影"}))
# output_key 可以指定输出的key
chain1 = LLMChain(llm=model, prompt=chat_prompt, output_parser=list_parser, verbose=True, output_key="output1")
chain2 = LLMChain(llm=model, prompt=chat_prompt2, output_parser=json_parser, verbose=True, output_key="output")

# Define input and output variables for the SequentialChain
chain = SequentialChain(
    chains=[chain1, chain2], 
    input_variables=["query","query2", "post","data"],
    output_variables=["output1", "output"],  # 可以指定多个输出的key 包括中间链的输出
    verbose=True
)
# test_data = read_file()
# result = chain.invoke({"data":test_data,"query": "请提取这段数据的标题", "query2": "请使用大概200字简短的概括一下这段数据","post": "思考模型"})
# print(result["output1"])
# print(result["output"])

"""
## create_sql_query_chain 默认的prompt
template = '''Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}.
Question: {question}
Question: {input}'''
"""
sql_chain = create_sql_query_chain(llm=model, db=db, get_col_comments=True)
result = sql_chain.invoke({"table_info": db.get_usable_table_names(), "question": f"查询存在订单的用户，使用{json_parser.get_format_instructions()} 格式的回答"})   
print("原始生成结果:", result)

# 解析结果，只提取SQL查询部分
# if result and "SQLQuery:" in result:
#     sql_query = result.split("SQLQuery:")[-1].strip()
#     # print("\n提取的SQL查询:", sql_query)
    
#     # 执行生成的SQL查询
#     db_result = db.run(sql_query)
#     print("\n数据库查询结果:", db_result)   







