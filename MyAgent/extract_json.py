import json
import re
from typing import List, Dict, Any

def extract_json_from_string(text: str) -> List[Dict[str, Any]]:
    """
    从字符串中提取JSON对象的更健壮方法
    """
    json_objects = []
    
    # 查找所有 { 的位置
    for match in re.finditer(r'\{', text):
        start = match.start()
        stack = 0
        pos = start
        
        # 找到匹配的 }
        while pos < len(text):
            if text[pos] == '{':
                stack += 1
            elif text[pos] == '}':
                stack -= 1
                if stack == 0:
                    # 找到了完整的JSON对象
                    json_str = text[start:pos+1]
                    try:
                        json_obj = json.loads(json_str)
                        json_objects.append(json_obj)
                        break
                    except json.JSONDecodeError:
                        pass
            pos += 1
    
    return json_objects

def extract_all_json_patterns(text: str) -> List[Dict[str, Any]]:
    """
    使用多种方法尝试提取JSON对象
    """
    results = []
    
    # 方法1: 使用栈方法
    results.extend(extract_json_from_string(text))
    
    # 方法2: 使用正则表达式查找可能的JSON模式
    # 这个正则表达式尝试匹配简单的JSON对象（非嵌套）
    simple_json_pattern = r'\{[^{}]*\}'
    simple_matches = re.findall(simple_json_pattern, text)
    
    for match in simple_matches:
        try:
            json_obj = json.loads(match)
            # 避免重复添加相同的JSON对象
            if json_obj not in results:
                results.append(json_obj)
        except json.JSONDecodeError:
            continue
    
    return results

def extract_python_dict(text: str) -> List[Dict[str, Any]]:
    """
    专门用于提取Python字典格式的函数
    """
    import ast
    
    json_objects = []
    
    # 尝试查找Python字典模式，使用更简单的方法
    # 找到所有以{开头的位置
    start_indices = []
    for i, char in enumerate(text):
        if char == '{':
            start_indices.append(i)
    
    # 对每个可能的开始位置尝试解析字典
    for start in start_indices:
        # 从这个位置开始尝试找到完整的字典
        stack = 0
        in_single_quote_str = False
        in_double_quote_str = False
        escape_next = False
        
        for pos in range(start, len(text)):
            char = text[pos]
            
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
            elif char == "'" and not in_double_quote_str and not escape_next:
                in_single_quote_str = not in_single_quote_str
            elif char == '"' and not in_single_quote_str and not escape_next:
                in_double_quote_str = not in_double_quote_str
            elif not in_single_quote_str and not in_double_quote_str:  # 只在字符串外部处理括号
                if char == '{':
                    stack += 1
                elif char == '}':
                    stack -= 1
                    if stack == 0:
                        # 找到了完整的Python字典
                        dict_str = text[start:pos+1]
                        try:
                            # 使用ast.literal_eval安全地解析Python字典
                            python_obj = ast.literal_eval(dict_str)
                            if isinstance(python_obj, (dict, list)):
                                if isinstance(python_obj, list):
                                    json_objects.extend(python_obj)
                                elif isinstance(python_obj, dict):
                                    json_objects.append(python_obj)
                            break
                        except (ValueError, SyntaxError):
                            pass
                        break
    return json_objects

def extract_json_with_regex(text: str) -> List[Dict[str, Any]]:
    """
    使用更健壮的方法提取JSON对象，处理嵌套对象
    """
    # 使用手动方法来处理嵌套的JSON对象
    json_objects = []
    i = 0
    while i < len(text):
        # Look for both { and [ to handle both objects and arrays
        if text[i] == '{' or text[i] == '[':
            start_char = text[i]
            end_char = '}' if start_char == '{' else ']'
            stack = 1
            start = i
            i += 1
            # 跟踪引号，确保不在字符串内部的括号被计算
            in_string_double = False
            in_string_single = False
            escape_next = False
            
            while i < len(text) and stack > 0:
                char = text[i]
                
                if escape_next:
                    escape_next = False
                elif char == '\\':
                    escape_next = True
                elif char == '"' and not escape_next and not in_string_single:
                    in_string_double = not in_string_double
                elif char == "'" and not escape_next and not in_string_double:
                    in_string_single = not in_string_single
                elif not in_string_double and not in_string_single:  # 只在字符串外部计算大括号/方括号
                    if char == start_char:
                        stack += 1
                    elif char == end_char:
                        stack -= 1
                i += 1
            
            if stack == 0:  # 完整的JSON对象或数组
                json_str = text[start:i]
                try:
                    json_obj = json.loads(json_str)
                    # If it's an array, add each object in the array to json_objects
                    if isinstance(json_obj, list):
                        json_objects.extend(json_obj)
                    elif isinstance(json_obj, dict):
                        json_objects.append(json_obj)
                except json.JSONDecodeError:
                    # 尝试修复常见的JSON问题
                    try:
                        # 修复可能的转义问题
                        fixed_json_str = json_str.replace('\\\\"', '\\"').replace('\\n', '\\\\n').replace('\\r', '\\\\r')
                        json_obj = json.loads(fixed_json_str)
                        # If it's an array, add each object in the array to json_objects
                        if isinstance(json_obj, list):
                            json_objects.extend(json_obj)
                        elif isinstance(json_obj, dict):
                            json_objects.append(json_obj)
                    except json.JSONDecodeError:
                        # 尝试将Python字典格式转换为JSON格式
                        try:
                            import ast
                            # 使用ast.literal_eval安全地解析Python字典（支持单引号）
                            python_obj = ast.literal_eval(json_str.strip())
                            if isinstance(python_obj, (dict, list)):
                                # 将Python对象转换为JSON兼容的对象
                                if isinstance(python_obj, list):
                                    json_objects.extend(python_obj)
                                elif isinstance(python_obj, dict):
                                    json_objects.append(python_obj)
                        except (ValueError, SyntaxError):
                            pass  # 无法解析，跳过
        else:
            i += 1
    
    return json_objects
# 提供一个简洁的函数，适用于大多数情况
def get_json_from_terminal_output(output: str) -> List[Dict[str, Any]]:
    """
    从终端输出中获取JSON数据的便捷函数
    """
    return extract_json_with_regex(output)

def get_formatted_json(output: str, indent: int = 2, ensure_ascii: bool = False) -> str:
    """
    从终端输出中获取格式化的JSON字符串
    
    Args:
        output: 终端输出字符串
        indent: 格式化缩进空格数，默认为2
        ensure_ascii: 是否确保ASCII字符，默认为False（支持中文等非ASCII字符）
    
    Returns:
        格式化的JSON字符串
    """
    json_objects = extract_json_with_regex(output)
    # 如果只有一个JSON对象，直接返回该对象的格式化字符串
    if len(json_objects) == 1:
        return json.dumps(json_objects[0], ensure_ascii=ensure_ascii, indent=indent)
    # 如果有多个JSON对象，返回包含所有对象的数组的格式化字符串
    elif len(json_objects) > 1:
        return json.dumps(json_objects, ensure_ascii=ensure_ascii, indent=indent)
    # 如果没有找到JSON对象， return an empty dict as a JSON string
    else:
        return json.dumps({}, ensure_ascii=ensure_ascii, indent=indent)



if __name__ == "__main__":
    # 示例使用
    terminal_output = """
    {
    'tool': 'write_file',
    'args': {
        'file_path': 'output.sql',
        'content': 'INSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1rpWjevEip\', \'【全748集】目前B站最全最细的<em class="keyword">Python</em>零基础全套教程，2024最 新版，包含所有干货！七天就能从小白到大神！少走99%的弯路！存下吧！很难找全的！\', \'【视频配套籽料、开发环境搭建安装包教程、电子书+问题解答请看 ”置顶平论” 自取哦】\', \'http://www.bilibili.com/video/av113006243481679\', 1724338758);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1P24y1m7LA\', \'猴博士【<em class="keyword">Python</em>】3小时不挂\', \'考试突击神器，可在3小时时间里，用最简单粗暴的方式，让你不挂科。\', \'http://www.bilibili.com/video/av690173570\', 1668587548);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1Sz4y1U77N\', \'20分钟学完一遍<em class="keyword">python</em>基础\', \'20分钟肯定是不够的，真正学会还需要我们动手实战演练。\', \'http://www.bilibili.com/video/av586659692\', 1613647025);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1qW4y1a7fU\', \'黑马程序员<em class="keyword">python</em>零基础全套教程，8天<em class="keyword">python</em>从入门到精通，学<em class="keyword">python</em>看这套就够了\', \'全部配套资源领取方式：关注黑马程序员公综 号，回复关键词:领取资源02\', \'http://www.bilibili.com/video/av941747210\', 1659920400);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1FWijBBEWa\', \'【2026最新】102个<em class="keyword">Python</em>实战项目，练完即可就业，从入门到进阶，基础到框架，你想要的全都有，建议码住！\', \'本视频仅用于网络爬虫教学，请遵守Robots.txt爬虫协议，严禁用于非法途径。\', \'http://www.bilibili.com/video/av115836056504342\', 1767518537);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1Jgf6YvE8e\', \'3小时超快速入门<em class="keyword">Python</em> | 动画教学【2025新版】【自学<em class="keyword">Python</em>教程】【 零基础<em class="keyword">Python</em>】【计算机二级<em class="keyword">Python</em>】【<em class="keyword">Python</em>期末速成】\', \'把Python教 程做成动画片了，教学通俗易懂，2025最新版，学完入门编程！\', \'http://www.bilibili.com/video/av113894261588276\', 1738401600);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1wD4y1o7AS\', \'花了2万多买的<em class="keyword">Python</em>教程全套，现在分享给大家，入门到精通(<em class="keyword">Python</em>全栈开发教程)\', \'【视频授权发布】视频为为Python中入门基础版(基础语法) 首次发布，最新版Python小白教程，从0开始，针对0基础小白和基础薄弱的伙伴学习，全程干货细讲\', \'http://www.bilibili.com/video/av712020469\', 1599479659);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV17G4y1U7jh\', \'<em class="keyword">Python</em>入门零基础必看教程，这绝对是今年最全最细的教程，全程干货无废话！<em class="keyword">python</em>|程序员|<em class="keyword">python</em>入门||人工智能|<em class="keyword">python</em>零基础\', \'Python 不是单一领域的语言，而是 “全栈型” 工具，主要应用在以下方向：\', \'http://www.bilibili.com/video/av863804481\', 1675563195);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1j8SYB1EgE\', \'信息技术会考 | <em class="keyword">Python</em>程序设计，看这一个就够了！（25年新版）\', \'高中信息技术会考Python程序设计完全攻略！\', \'http://www.bilibili.com/video/av115654862637085\', 1764753554);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1xHn9z8EPX\', \'<em class="keyword">Python</em>入门半小时，剩下靠AI\', \'\', \'http://www.bilibili.com/video/av115279304595500\', 1759022996);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV15J411T7WQ\', \'千锋教育<em class="keyword">Python</em>全套视频教程800集（完整版）\', \'千锋教育Python全套精品教程： 基础+进阶+高 级+项目+知识点总结，全套800集完整版（学完可就业/入门到精通），全网最全&官方版本，名师精讲，最适合零基础小白学习的python视频。\', \'http://www.bilibili.com/video/av69060979\', 1569514497);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1VT4y1v7oe\', \'高中信息合格考<em class="keyword">Python</em>编程突击课\', \'我从来只做高质量教程，我确保每一次的教程都是最浅白的语言，我确保每一次的视频都是1080P全高清，我确保每一句话都字正腔圆，用我对自我的苛求满足你的进取心。\', \'http://www.bilibili.com/video/av937870160\', 1648941387);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1c4411e77t\', \'【<em class="keyword">Python</em>教程】《零基础入门学习<em class="keyword">Python</em>》最新版（完结撒花🎉）\', \'本系列教程是《零基础入门学习Python》最新版教程，希望大家喜欢。\', \'http://www.bilibili.com/video/av52080698\', 1557527581);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1ng4y1i7Uk\', \'全球最强<em class="keyword">python</em>教程--mosh大神的<em class="keyword">python</em>从入门到精通-完整版来了 一共13节-715分钟-请谨慎观看！\', \'转自http://codewithmosh.com/\', \'http://www.bilibili.com/video/av838838220\', 1594653966);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1vs29BZEzG\', \'【全748 集】清华大佬终于把<em class="keyword">Python</em>全套教程讲完了！入门到实战全新讲解，一个月带你小白变大神！（程序员|<em class="keyword">Python</em>入门零基础|网络爬虫|数据分析）\', \'【视频配套籽料、开发环境搭建安装包教程、电子书+问题解答请看 ”置顶平论” 自取哦】\', \'http://www.bilibili.com/video/av115672243765547\', 1765029900);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1AdivBbEVN\', \'【全549集】2026最细自学<em class="keyword">Python</em>全套教程，全程干货无废话！学完即可就业，从零基础小白进阶到<em class="keyword">Python</em>大神看这套就够了！存下吧，很难找全的！！\', \'本套教程包含了语法基础、语法进阶、巩固练习题、网络爬虫、数据分析、自动化办公等，全程通俗易懂。无论你是零基础小白，还是有一定的编码能力，皆可学习！\', \'http://www.bilibili.com/video/av115830335476856\', 1767438795);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1gt4y1D7W8\', \'【全集】孙兴华《中文讲<em class="keyword">Python</em>从入门到办公自动化》excel、word、ppt、PDF等 <em class="keyword">Python</em>自动化 <em class="keyword">Python</em>办 公自动化 <em class="keyword">Python</em>自动化办公\', \'很多人都在问办公自动化的学习路线，其实不用全都学，我把全部路线整理出来了，因为很多东西，比如装饰器、闭包、面向对象等都是程序员才会用到，办公自动化很简单，不需要学习这些知识同样可以操作。按这个视频的路线学习即可\', \'http://www.bilibili.com/video/av626573992\', 1595857129);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1z5411R7az\', \'<em class="keyword">Python</em>能做什么？二十分钟带你了解<em class="keyword">Python</em>真正用途\', \'\', \'http://www.bilibili.com/video/av468719735\', 1651424400);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1T4isBBEpL\', \'【中配】五个好的<em class="keyword">Python</em>习惯 - Indently\', \'原视频：5 Good Python Habits\', \'http://www.bilibili.com/video/av115841173559412\', 1767596363);\nINSERT INTO ai_blbl (video_id, video_title, video_description, video_url, video_publish_time) VALUES (\'BV1JmiLBPEmL\', \'假如你从1月开始自学<em class="keyword">Python</em>编程技术，能救一个是一个！！！\', \'\', \'http://www.bilibili.com/video/av115836190922652\', 1767520238);'
    },
    'message': '正在将SQL语句写入output.sql文件'
}

    """

    print("方法1 - 使用栈方法提取JSON:")
    json_data1 = extract_json_from_string(terminal_output)
    for obj in json_data1:
        print(json.dumps(obj, ensure_ascii=False, indent=2))

    print("\n方法2 - 使用多种方法提取JSON:")
    json_data2 = extract_all_json_patterns(terminal_output)
    for obj in json_data2:
        print(json.dumps(obj, ensure_ascii=False, indent=2))

    print("\n方法3 - 使用递归式正则方法提取JSON:")
    json_data3 = extract_json_with_regex(terminal_output)
    for obj in json_data3:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    print("\n使用便捷函数提取JSON:")
    json_data_simple = get_json_from_terminal_output(terminal_output)
    for obj in json_data_simple:
        print(json.dumps(obj, ensure_ascii=False, indent=2))

    print("\n获取格式化的JSON字符串:")
    formatted_json = get_formatted_json(terminal_output)
    print(json.loads(formatted_json, strict=False))