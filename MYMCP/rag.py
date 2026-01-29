from typing import List
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity
import os ,json
import time
from pathlib import Path
from mcpServer import mcp  # 统一的MCP实例，包含B站搜索和ModelScope API
import asyncio
import speak

import chromadb

# 设置更大的下载限制
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '1200'  # 20分钟超时
os.environ['HF_HUB_MAX_RETRIES'] = '10'        # 最大重试次数
os.environ['HF_HUB_DOWNLOAD_CHUNK_SIZE'] = '1048576'  # 1MB块大小
# 设置环境变量以使用镜像源（如果可用）
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # 例如使用镜像源
'''
使用HuggingFace的SentenceTransformer模型进行文本向量化和相似度计算
中文文本 → [model.encode()] → 向量表示 → [相似度计算] → 相似度分数

召回：根据查询向量与所有段落向量的余弦相似度，返回最相似的段落
重排: 根据查询向量和段落向量之间的余弦相似度，返回最相似的段落

'''

# chromadb_client = chromadb.EphemeralClient()
chromadb_client = chromadb.PersistentClient(path="./chroma_db") ## 持久化
collection = chromadb_client.get_or_create_collection("news")

## 模型加载
def load_model_with_retry(model_name="shibing624/text2vec-base-chinese", max_retries=3):
    """
    带重试机制的模型加载函数
    """
    # 设置环境变量使用镜像
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    
    # 构建本地模型路径
    cache_path = Path("./cache")
    model_cache_path = cache_path / f"models--{model_name.replace('/', '--')}"
    
    # 如果本地缓存存在，直接从本地加载
    if model_cache_path.exists():
        # 获取最新的快照目录
        snapshots_path = model_cache_path / "snapshots"
        if snapshots_path.exists():
            # 获取快照目录下的第一个（也是唯一一个）目录
            snapshot_dirs = [d for d in snapshots_path.iterdir() if d.is_dir()]
            if snapshot_dirs:
                local_model_path = snapshot_dirs[0]
                print(f"🔍 检测到本地缓存，从 {local_model_path} 加载模型...")
                # print(f"⚠️  注意：请确保本地缓存目录下只有一个模型版本！:{str(local_model_path)}")
                try:
                    model = SentenceTransformer(
                        str(local_model_path),
                        trust_remote_code=True,
                        cache_folder="./cache",
                    )
                    print("✅ 从本地缓存加载模型成功！")
                    return model
                except Exception as e:
                    print(f"❌ 从本地缓存加载失败: {e}")
    
    # 如果本地加载失败或不存在，则尝试使用远程名称（带缓存）
    for attempt in range(max_retries):
        try:
            print(f"尝试加载模型 (第 {attempt + 1} 次)...")
            
            model = SentenceTransformer(
                model_name,
                trust_remote_code=True,
                cache_folder="./cache",
            )
            
            print("✅ 模型加载成功！")
            return model
            
        except Exception as e:
            print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
            
            if attempt < max_retries - 1:
                print(f"⏳ 等待后重试...")
                time.sleep(5)  # 等待5秒后重试
            else:
                print("💥 所有重试都失败了")
                raise e
## 文本分割
def split_into_chunks(doc_file: str) -> List[str]:
    with open(doc_file, 'r', encoding='utf-8') as file:
        content = file.read()

    chunks = [chunk for chunk in content.split("\n\n") if chunk.strip()]
    # for i, chunk in enumerate(chunks):
    #     print(f"[{i}] {chunk}\n")
    print(f"分段数：{len(chunks)}")
    return chunks

## 保存向量
def save_embeddings(chunks:List[str], embeddings):

    ids = [str(i) for i in range(len(chunks))]
    
    # Ensure embeddings is in the correct format (list of lists)
    # If we have a single chunk but embeddings is a 1D array, wrap it
    if len(chunks) == 1 and len(embeddings) > 0 and not isinstance(embeddings[0], list):
        embeddings = [embeddings]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
    result = collection.get(ids=ids, include=['embeddings', 'documents'])
    print(f"✅ 向量保存成功！{len(result['embeddings'])}")

 ## 向量查询
def calculate_similarity(query: str, chunks: List[str], model: SentenceTransformer, top_k: int = 5):
    # Encode the query
    query_embedding = model.encode([query])  # Wrap in a list to get 2D array
    # chunk_embeddings = model.encode(chunks)
    chunk_embeddings = collection.get(ids=[str(i) for i in range(len(chunks))], include=['embeddings'])['embeddings']
    
    # Calculate cosine similarity between query and chunks
      # 根据查询向量与所有段落向量的余弦相似度，返回最相似的段落
    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]
    top_indices = similarities.argsort()[::-1][:top_k]
    return [chunks[i] for i in top_indices]
## 向量召回
def query_embeddings(query: str, chunks: List[str], model: SentenceTransformer, top_k: int = 5) -> List[str]:
    print(f"查询：{query}")
    query_embedding = model.encode([query])  # Wrap in a list to get 2D array
    # chunk_embeddings = collection.get(ids=[str(i) for i in range(len(chunks))], include=['embeddings'])['embeddings']
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=['documents', 'embeddings']
    )
    # print(f"查询结果：{results}")
    return results['documents'][0]

## 重排
def rerank(query: str, retrieved_chunks: List[str], top_k: int) -> List[str]:
    from pathlib import Path
    
    # 构建本地模型路径
    model_name = 'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'
    cache_path = Path("./cache")
    model_cache_path = cache_path / f"models--{model_name.replace('/', '--')}"
    
    # 如果本地缓存存在，直接从本地加载
    cross_encoder = None
    if model_cache_path.exists():
        # 获取最新的快照目录
        snapshots_path = model_cache_path / "snapshots"
        if snapshots_path.exists():
            # 获取快照目录下的最新目录
            snapshot_dirs = [d for d in snapshots_path.iterdir() if d.is_dir()]
            if snapshot_dirs:
                # 按修改时间排序，获取最新的快照
                latest_snapshot = max(snapshot_dirs, key=lambda x: x.stat().st_mtime)
                local_model_path = latest_snapshot
                print(f"🔍 检测到本地重排模型缓存，从 {local_model_path} 加载...")
                try:
                    cross_encoder = CrossEncoder(
                        str(local_model_path),
                        trust_remote_code=True,
                        cache_folder="./cache"
                    )
                    print("✅ 从本地缓存加载重排模型成功！")
                except Exception as e:
                    print(f"❌ 从本地缓存加载重排模型失败: {e}")
    
    # 如果本地加载失败或不存在，则尝试下载
    if cross_encoder is None:
        # 设置环境变量以使用镜像源和增加下载超时
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
        os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '1200'  # 20分钟超时
        os.environ['HF_HUB_MAX_RETRIES'] = '10'        # 最大重试次数
        os.environ['HF_HUB_DOWNLOAD_CHUNK_SIZE'] = '1048576'  # 1MB块大小
        
        # 带重试机制的CrossEncoder加载
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"尝试加载重排模型 (第 {attempt + 1} 次)...")
                cross_encoder = CrossEncoder(model_name, trust_remote_code=True, cache_folder="./cache")
                print("✅ 重排模型加载成功！")
                break
            except Exception as e:
                print(f"❌ 第 {attempt + 1} 次尝试加载重排模型失败: {e}")
                if attempt == max_retries - 1:  # 最后一次尝试也失败了
                    print("⚠️  重排模型加载失败，跳过重排步骤，直接返回检索结果")
                    return retrieved_chunks[:top_k]  # 直接返回前top_k个检索结果
    
    pairs = [(query, chunk) for chunk in retrieved_chunks]
    scores = cross_encoder.predict(pairs)

    scored_chunks = list(zip(retrieved_chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    # print(f"重排结果：{scored_chunks}")

    return [chunk for chunk, _ in scored_chunks][:top_k]


## 调用大模型
async def mcp_chat(query: str, chunks: List[str]):
    print(f"chat模型调用 问题：{query}")
    # 构建提示词，避免f-string中的多行字符串问题
    related_chunks = "\n\n".join(chunks)
    summary_prompt = f'''你是一位知识助手，请根据用户的问题和下列片段生成准确的回答。
        用户问题: {query}
        相关片段:
        {related_chunks}
        请基于上述内容作答，不要编造信息。'''
    # await 只能在异步函数中使用，此处需改为同步调用或包装为异步函数
    summary_result = await mcp.call_tool("modelscope_chat_completion", {
        "prompt": summary_prompt,
        "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "temperature": 0.7,
        # "max_tokens": 200
    })
    # print(summary_result)
    summary_content = summary_result[0][0].text
    result_dict = json.loads(summary_content) if isinstance(summary_content, str) else summary_content
    print(result_dict)
    content = result_dict.get("content", "") if isinstance(result_dict, dict) else ""
    print(f"  ✅ AI总结完成")
    return content

if __name__ == "__main__":
    chunks = split_into_chunks("news.txt")
    model = load_model_with_retry()
    
    embeddings = model.encode(chunks).tolist()
    save_embeddings(chunks, embeddings)

    query = "美国的战略"
    results = query_embeddings(query, chunks, model, top_k=100)
    # similarities = calculate_similarity(query, results, model, top_k=100)   
    # print(f"相似度：{similarities}")

    # print(f"重排前{results}")
    results = rerank(query, results, top_k=5)
    # print(f"重排后{results}")
    for i, result in enumerate(results):
        print(f"[{i}] {result}\n")

    # summary_content = asyncio.run(mcp_chat(query, chunks))
    # print(summary_content)
    # with open("summary.md", "w", encoding="utf-8") as f:
    #     f.write(summary_content)
    # asyncio.run(speak.generate_speech(file_path="summary.md", output_file="summary.mp3"))
