import translators as ts

# 最简单的用法
# print(ts.translators_pool)
# 通用接口，通过 translator 参数指定引擎
result = ts.translate_text(
    "通用接口，通过 translator 参数指定引擎", 
    translator='caiyun',  # 指定使用百度
    from_language='zh', 
    to_language='en'
)
print(result)  # 你好，世界

def translate_file_simple(input_file, output_file, from_lang='en', to_lang='zh'):
    engines = ['bing', 'youdao', 'sougou', 'deepl']
    """
    简单文件翻译（一次性读取整个文件）
    """
    for engine in engines:
        try:
            # 读取文件
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 翻译
            translated = ts.translate_text(
                content,
                translator= engine,  # 可以换成 'bing', 'baidu', 'youdao' 等
                from_language=from_lang,
                to_language=to_lang
            )
            
            # 保存结果
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated)
            
            print(f"翻译完成！已保存到 {output_file}")
            break
            
        except Exception as e:
            print(f"翻译失败：{e}")
            continue



translate_file_simple('summary.md', 'output.txt', from_lang='zh', to_lang='en')