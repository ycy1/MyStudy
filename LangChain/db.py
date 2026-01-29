from langchain_community.utilities import SQLDatabase

# 连接 MySQL 数据库
db_user = "root" 
db_password = "root"
  
#根据自己的密码填写
db_host = "127.0.0.1" 
db_port = "3306" 
db_name = "fastapi_db"
# mysql+pymysql://用户名:密码@ip地址:端口号/数据库名
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

if __name__ == "__main__":
    print("哪种数据库：", db.dialect)
    print("获取数据表：", db.get_usable_table_names())
    # print("获取表结构：", db.table_info)
    # 执行查询
    res = db.run("SELECT username FROM user;")
    print("查询结果：", res)

