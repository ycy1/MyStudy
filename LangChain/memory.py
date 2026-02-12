from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains.llm import LLMChain
from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.memory import ConversationBufferWindowMemory,ConversationTokenBufferMemory,ConversationSummaryBufferMemory,ConversationSummaryMemory,ConversationEntityMemory,VectorStoreRetrieverMemory
from langchain_classic.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

from langchain_classic.chains.sequential import SequentialChain
from langchain_classic.memory.buffer import ConversationBufferMemory  # 或者从其他正确的位置导入
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import history

from model import model,model_ollama
from rag import load_model_with_retry

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个问答机器人，请回答我的问题。"),
    # ("system", "历史消息：{history}"),
    MessagesPlaceholder(variable_name="history"), ## 插值构造器 加入历史消息
    ("human", "{query}"),
])

history = ChatMessageHistory()
history.add_user_message("你好呀!")
history.add_ai_message("你好! 我是一个专业的问答机器人，你可以向我咨询任何问题。")  
# print(history.messages) 

memory = ConversationBufferMemory(memory_key="history", return_messages=False)
memory.save_context({"input": "你好呀!"}, {"output": "你好! 我是一个专业的问答机器人，你可以向我咨询任何问题。"})
memory.save_context({"input": "周星驰的电影!"}, {"output": "周星驰的电影有很多，比如《喜剧之王》、《大话西游》、《大话西游2》等。"})
memory.save_context({"input": "周星驰是哪里人?"}, {"output": "周星驰是香港人。"})   

# print(type(memory.load_memory_variables({})))
# print(memory.load_memory_variables({})["myKey"])
# memoryRes = memory.load_memory_variables({})["myKey"]
# memoryRes = memory.chat_memory.messages
# print(memory.load_memory_variables({}))
# promptRes = prompt.format_prompt(history=memoryRes, query="总结一下我们的对话内容")
# print(promptRes)

# chain = prompt | model
# res = chain.invoke({"query": "简短的总结一下我们的对话内容"})
# print(res.content) 

## 内部使用memory.load_memory_variables({}) 方式获取memory的key作为输入传递给prompt
# chain1 = LLMChain(llm=model, prompt=prompt, memory=memory, output_key="output1")
# res = chain1.invoke({"query": "简短的总结一下我们的对话内容"})
# print(res["output1"]) 
#PROMPT = PromptTemplate(input_variables=["history", "input"], template=DEFAULT_TEMPLATE)

# chain = ConversationChain(llm=model_ollama,prompt=prompt,input_key="query")
# chain.predict(query="简短的总结一下我们的对话内容")  ## 加入对话
# chain.memory.return_messages = True ## 设置默认memory的返回格式为messages 而不是string
## 默认prompt是PromptTemplate类型 input_variables 为 ["history", "input"]
# print(type(chain.prompt))
# chain.prompt.input_variables = ["history", "query"]
# chain.prompt.template = prompt.template
# memory = ConversationBufferWindowMemory(k=1,memory_key="history",return_messages=True) 
# chain = ConversationChain(llm=model_ollama,prompt=prompt,memory=memory,input_key="query")

# res2 = chain.invoke({"query": "周星驰的电影有哪些?"})
# print(res2["history"])
# res = chain.invoke({"query": "简短的总结一下我们的对话内容"})
# print(res["history"])
# res = chain.invoke({"query": "我们进行了几轮对话?"})
# print(res["history"])

# memory2 = ConversationSummaryMemory(llm=model,return_messages=True,memory=memory) 
# memory2.save_context({"input": "介绍一下周星驰?"}, {"output": "周星驰是一个香港人，他的电影有很多，比如《喜剧之王》、《大话西游》、《大话西游2》等。"})
# memory2.save_context({"input": "周星驰的电影有哪些?"}, {"output": "周星驰的电影有很多，比如《喜剧之王》、《大话西游》、《大话西游2》等。"})
# memory2.save_context({"input": "周星驰是哪里人?"}, {"output": "周星驰是香港人。"})
# memory2 = ConversationSummaryMemory.from_messages(llm=model,chat_memory=history) ## 基于已有的messages 生成summary
# print(memory2.load_memory_variables({})) 
# print(memory2.chat_memory.messages) ## 获取memory中的交互过程
## 基于已有的messages 生成summary 并限制token数量
# memory3 = ConversationSummaryBufferMemory(llm=model_ollama,chat_memory=history,max_token_limit=200,return_messages=True) 
# memory3.save_context({"input": "介绍一下周星驰?"}, {"output": "周星驰是一个香港人，他的电影有很多，比如《喜剧之王》、《大话西游》、《大话西游2》等。"})
# memory3.save_context({"input": "周星驰的电影有哪些?"}, {"output": "周星驰的电影有很多，比如《喜剧之王》、《大话西游》、《大话西游2》等。"})
# memory3.save_context({"input": "周星驰是哪里人?"}, {"output": "周星驰是香港人。"})
# print(memory3.load_memory_variables({})) 
# print("\n")
# print(memory3.chat_memory.messages) ## 获取memory中的交互过程,超过指定token数量 会自动截断

memory4 = ConversationEntityMemory(llm=model,input_key="input",return_messages=True)

# entity_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个问答机器人，请回答我的问题。{entities}"),
#     MessagesPlaceholder(variable_name="history"), ## 插值构造器 加入历史消息
#     ("human", "{input}"),
# ])

# chain = ConversationChain(llm=model,prompt=entity_prompt,memory=memory4,input_key="query")

# chain = ConversationChain(
#     llm=model,
#     memory=memory4,
#     prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
#     # verbose=True  # 查看详细过程
# )

# # 进行对话
# result1 = chain.invoke({"input": "我叫张三，今年25岁，在北京工作。"})
# print(result1,"\n")

# result2 = chain.invoke({"input": "我喜欢编程和游泳。"})
# print(result2,"\n")
# print("存储的实体:", memory4.entity_store.store,"\n")

# # 询问关于实体的信息
# result3 = chain.invoke({"input": "我刚才说我叫什么名字？多大了？"})         
# print(result3,"\n")
# print(memory4.chat_memory.messages)
# print(memory4.load_memory_variables({"input": "我刚才说我叫什么名字？多大了？"}),"\n")
from langchain_community.memory.kg import ConversationKGMemory
# memory5 = ConversationKGMemory(llm=model)
# memory5.save_context({"input": "介绍一下周星驰?"}, {"output": "周星驰是一个香港人，他的电影有很多，比如《喜剧之王》、《大话西游》、《大话西游2》等。"})
# memory5.save_context({"input": "周星驰的电影有哪些?"}, {"output": "周星驰的电影有很多，比如《喜剧之王》、《大话西游》、《大话西游2》等。"})
# memory5.save_context({"input": "周星驰是哪里人?"}, {"output": "周星驰是香港人。"})
# print(memory5.load_memory_variables({"input": "周星驰是哪里人?"}),"\n")
# print(memory5.get_knowledge_triplets("周星驰是哪里人?"))
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

# Create a wrapper class for SentenceTransformer to implement LangChain Embeddings interface
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model):
        self.model = model
    
    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()
    
    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

embeddings_model = load_model_with_retry()
# Wrap the SentenceTransformer model
langchain_embeddings = SentenceTransformerEmbeddings(embeddings_model)
# print(memory.buffer)  
vectorstore = FAISS.from_texts(memory.buffer.split("\n"), langchain_embeddings)
# Create a retriever from the FAISS vectorstore
# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
# memory6 = VectorStoreRetrieverMemory(llm=model,retriever=retriever,memory_key="history",return_messages=True)
# # print(memory6.load_memory_variables({"input": "周星驰的电影有哪些?"}),"\n")  
# print(retriever.invoke("电影?"))  






