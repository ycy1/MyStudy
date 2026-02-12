from langchain_core.output_parsers import JsonOutputParser, StrOutputParser,XMLOutputParser,CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate

from model import model,model_ollama

## 每个解析器都有 get_format_instructions函数
json_parser = JsonOutputParser()
xml_parser = XMLOutputParser()
list_parser = CommaSeparatedListOutputParser()

# print(xml_parser.get_format_instructions())
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", f"你是一个专业的问答机器人，使用{xml_parser.get_format_instructions()}格式的回答"),
    ("human", "{query}"),
])

# prompt = PromptTemplate(
#     template="回答用户的查询.\n\n{query}\n",
#     input_variables=["query"],
#     # partial_variables={"format_instructions": parser.get_format_instructions()},
# )



# print(xml_parser.get_format_instructions())
# \n{xml_parser.get_format_instructions()}\n
pro_res = chat_prompt.invoke({"query": f"你好,周星驰是谁"})
for chunk in model_ollama.stream(pro_res):   
    print(chunk.content, end="", flush=True)
# print(f"{res.content}")

# parser = StrOutputParser()
# print(parsed_res.to_json())  
# print(list_parser.invoke(res))   

# print(json_parser.get_format_instructions())
# print(json_parser.invoke(res))

## 链式调用 管道符分割 按顺序传递返回， 每个对象必须存在所调函数,传参为首位对象的入参
# chain = chat_prompt | model | json_parser 
# print(chain.invoke({"query": f"你好,{json_parser.get_format_instructions()}"}))

# chain = chat_prompt | model | xml_parser 
# print(chain.invoke({"query": f"你好,请输出周星驰的电影"}))

# chain = chat_prompt | model | list_parser
# print(chain.invoke({"query": f"你好,请输出周星驰的电影"}))
