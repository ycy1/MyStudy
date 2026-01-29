from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import time
from pathlib import Path
'''
使用HuggingFace的SentenceTransformer模型进行文本向量化和相似度计算
中文文本 → [model.encode()] → 向量表示 → [相似度计算] → 相似度分数
'''
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

def test_model_functionality(model):
    """
    测试模型功能
    """
    sentences =["今天天气真好","晴天万里","我非常开心","我的工作是互联网","我的兴趣爱好是旅游"]   
    ask = ["你今天的心情怎么样"]
    print(f"ask:{ask}")
    
    print("🔍 测试模型编码功能...")
    embeddings = model.encode(sentences)
    print(f"✅ 编码完成，嵌入向量维度: {embeddings.shape}")
    print("🔍 测试模型相似度计算...")
    ask_embedding = model.encode(ask)
    similarities = cosine_similarity(embeddings, ask_embedding)
    print(f"✅ 模型相似度计算完成，相似度矩阵形状:{similarities.shape}\n {similarities}")

    ## 获取最相似的句子
    best_match_index = similarities.argmax()
    # print(f"✅ 最相似的句子索引是: {best_match_index}")
    best_match_sentence = sentences[best_match_index]
    print(f"✅ 最相似的句子是: {best_match_sentence}")
    
    return best_match_sentence

if __name__ == "__main__":
    try:
        model = load_model_with_retry()
        print("🎉 模型加载完成！")
        
        # 测试模型功能
        best_match_sentence = test_model_functionality(model)
        
        print("\n✅ 所有测试通过！模型可以正常使用。")
        
    except Exception as e:
        print(f"\n❌ 加载模型失败: {e}")
        print("\n💡 建议解决方案:")
        print("   1. 检查网络连接")
        print("   2. 确保有足够的磁盘空间")
        print("   3. 如果网络不稳定，可以尝试使用代理")
        print("   4. 手动从 https://hf-mirror.com 下载模型文件")