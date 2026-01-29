import json

if __name__ == "__main__":
    ## 读取文件
    with open("output.txt", "r", encoding="utf-8") as f:

        content = f.read()
        print(content)
        model_reply = json.loads(content, strict=False)
        print(model_reply)
