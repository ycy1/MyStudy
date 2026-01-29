"""
演示大语言模型自主判断调用B站工具的场景
"""
import asyncio
import json
import time
import os
from mcpServer import mcp  # 统一的MCP实例，包含B站搜索和ModelScope API

async def demonstrate_autonomous_decision():
    """演示大模型如何自主判断调用B站工具"""
    print("🤖 大模型自主判断调用B站工具演示")
    print("="*60)
    
    # 场景1: 用户询问视频教程相关问题 - 大模型应该调用B站搜索
    print("\n🔍 场景1: 寻找Python教程视频")
    query = "Python教程"
    print(f"  用户问题: 寻找关于{query}的视频教程")
    
    # 模拟大模型判断需要调用B站搜索
    print(f"  AI判断: 需要查找视频教程内容，调用B站搜索工具")
    start_time = time.time()
    try:
        result = await mcp.call_tool("blbl", {"keyword": query})
        end_time = time.time()
        print(f"  ✅ B站搜索成功 (耗时: {end_time - start_time:.3f}s)")
        
        # 简单处理结果
        if isinstance(result, dict) and 'data' in result:
            video_count = result['data'].get('numResults', 0) if result['data'] else 0
            print(f"  📺 找到 {video_count} 个相关视频")
        else:
            print(f"  📺 B站搜索返回了结果")
    except Exception as e:
        print(f"  ❌ B站搜索失败 - {e}")

    
    # 场景3: 复合任务 - 先搜索B站视频，再用AI总结
    print("\n🔗 场景3: 复合任务 - 搜索并总结")
    search_keyword = "Python教程"
    print(f"  用户需求: 找到关于'{search_keyword}'的视频，然后总结相关内容")
    
    # 第一步：调用B站搜索
    print(f"  AI判断: 首先需要搜索相关视频内容")
    start_time = time.time()
    try:
        bili_result = await mcp.call_tool("blbl", {"keyword": search_keyword})
        # print(f"  📺 找到 {bili_result}")
        end_time = time.time()
        print(f"  ✅ B站搜索完成 (耗时: {end_time - start_time:.3f}s)")
        
        # 第二步：如果有ModelScope API密钥，用AI总结搜索结果
        if os.getenv("MODELSCOPE_API_KEY"):
            print(f"  AI判断: 搜索完成，现在用AI总结搜索结果")
            summary_prompt = f"请根据以下B站搜索结果，列出{search_keyword}的学习热门视频和具体链接：{str(bili_result)}。"
            
            start_time = time.time()
            try:
                summary_result = await mcp.call_tool("modelscope_chat_completion", {
                    "prompt": summary_prompt,
                    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
                    "temperature": 0.7,
                    # "max_tokens": 200
                })
                end_time = time.time()
                
                # Handle different possible return types from modelscope_chat_completion
                summary_content = ""
                
                if isinstance(summary_result, dict):
                    if "content" in summary_result:
                        summary_content = summary_result["content"]
                    elif "error" in summary_result:
                        print(f"  ❌ AI总结错误: {summary_result['error']}")
                        summary_content = f"Summary failed: {summary_result['error']}"
                    else:
                        summary_content = str(summary_result)
                elif isinstance(summary_result, tuple) and len(summary_result) > 0:
                    # Handle tuple response
                    if hasattr(summary_result[0][0], 'text'):
                        summary_content = str(summary_result[0][0].text)
                    else:
                        summary_content = str(summary_result)
                else:
                    # Handle any other type
                    summary_content = str(summary_result)
                
                print(f"  ✅ AI总结完成 (耗时: {end_time - start_time:.3f}s)")
                print(f"  📝 总结预览: {summary_content}")

                ## 保存总结
                print(f"  📥 正在保存总结到数据库...")
                try:
                    # Create table if it doesn't exist
                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS ai_summaries (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        summary TEXT NOT NULL,
                        search_keyword VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                    create_result = await mcp.call_tool("db_server", {"query": create_table_query})
                    
                    # Extract the actual result from the tuple if needed
                    actual_create_result = create_result
                    if isinstance(create_result, tuple) and len(create_result) >= 2:
                        # The actual result is in the second element of the tuple
                        actual_create_result = create_result[1].get('result', {}) if isinstance(create_result[1], dict) else {}
                    elif isinstance(create_result, tuple) and len(create_result) >= 1:
                        # If only one element, try to extract from the first element
                        first_elem = create_result[0]
                        if isinstance(first_elem, list) and len(first_elem) > 0:
                            # Extract from TextContent
                            text_content = first_elem[0]
                            import json
                            try:
                                # Try to parse the text content as JSON
                                actual_create_result = json.loads(text_content.text)
                            except:
                                actual_create_result = {}
                        elif isinstance(first_elem, dict):
                            actual_create_result = first_elem
                    
                    # Check if the operation was successful
                    if isinstance(actual_create_result, dict) and actual_create_result.get("success"):
                        print(f"  ✅ 表创建成功或已存在")
                    else:
                        error_msg = actual_create_result.get('error', 'Unknown error') if isinstance(actual_create_result, dict) else 'Unknown error'
                        print(f"  ❌ 表创建失败: {error_msg}")
                    
                    # Insert the summary into the database
                    # Escape single quotes in the content to prevent SQL injection
                    escaped_summary = summary_content.replace("'", "''")
                    escaped_keyword = search_keyword.replace("'", "''")
                    insert_query = f"""
                    INSERT INTO ai_summaries (summary, search_keyword) 
                    VALUES ('{escaped_summary}', '{escaped_keyword}')
                    """
                    insert_result = await mcp.call_tool("db_server", {"query": insert_query})
                    
                    # Extract the actual result from the tuple if needed
                    actual_insert_result = insert_result
                    if isinstance(insert_result, tuple) and len(insert_result) >= 2:
                        # The actual result is in the second element of the tuple
                        actual_insert_result = insert_result[1].get('result', {}) if isinstance(insert_result[1], dict) else {}
                    elif isinstance(insert_result, tuple) and len(insert_result) >= 1:
                        # If only one element, try to extract from the first element
                        first_elem = insert_result[0]
                        if isinstance(first_elem, list) and len(first_elem) > 0:
                            # Extract from TextContent
                            text_content = first_elem[0]
                            import json
                            try:
                                # Try to parse the text content as JSON
                                actual_insert_result = json.loads(text_content.text)
                            except:
                                actual_insert_result = {}
                        elif isinstance(first_elem, dict):
                            actual_insert_result = first_elem
                    
                    # Check if the operation was successful
                    if isinstance(actual_insert_result, dict) and actual_insert_result.get("success"):
                        print(f"  ✅ 总结已保存到数据库")
                    else:
                        error_msg = actual_insert_result.get('error', 'Unknown error') if isinstance(actual_insert_result, dict) else 'Unknown error'
                        print(f"  ❌ 保存失败: {error_msg}")
                except Exception as e:
                    print(f"  ❌ 保存总结到数据库时出错: {e}")
                    
            except Exception as e:
                print(f"  ❌ AI总结失败 - {e}")
        else:
            print("  ⚠️  ModelScope API密钥未设置，跳过AI总结")
            print("  要运行此测试，请设置环境变量 MODELSCOPE_API_KEY")
            
    except Exception as e:
        print(f"  ❌ B站搜索失败 - {e}")
    
    print("\n" + "="*60)
    print("🎯 演示完成！展示了大模型如何自主判断调用不同工具")

if __name__ == "__main__":
    asyncio.run(demonstrate_autonomous_decision())