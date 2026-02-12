## pip install tortoise-orm==0.25.0 aerich==0.9.0 aiomysql==0.2.0 tomlkit==0.13.2

## aerich init -t dbConfig.TORTOISE_ORM_CONFIG
## aerich init-db  初始化
## aerich migrate  创建迁移文件
## aerich upgrade  同步数据库
## aerich downgrade -v <version>  回滚数据库
## aerich history  查看迁移历史

from tortoise.models import Model
from tortoise.fields import CharField,BooleanField,IntField,OneToOneField,ForeignKeyField,CASCADE,BigIntField

class User(Model):
    id = BigIntField(pk=True, auto_increment=True)
    username = CharField(max_length=255, null=True)
    password = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
    address = CharField(max_length=255, null=True)
    nickname = CharField(max_length=255, null=True)
    info = OneToOneField(null=True,model_name="models.UserInfo", on_delete=CASCADE, related_name="user")

    class Meta:
        table = "user"
        ordering = ["username"]

    # def __str__(self):
    #     return self.username
    

class UserInfo(Model):
    id = BigIntField(pk=True, auto_increment=True)
    cid = CharField(max_length=255)

    class Meta:
        table = "user_info"
        ordering = ["cid"]

    def __str__(self):
        return self.cid

class Order(Model):
    id = BigIntField(pk=True, auto_increment=True)
    name = CharField(max_length=255)
    user = ForeignKeyField("models.User", related_name="orders", on_delete=CASCADE, to_field="id")
    
    class Meta:
        table = "order"
        ordering = ["id"]

  

class Post(Model):
    id = BigIntField(pk=True, auto_increment=True)
    name = CharField(max_length=255)

class UserPost(Model):
    id = BigIntField(pk=True, auto_increment=True)
    user = ForeignKeyField("models.User", related_name="models.userPost", on_delete=CASCADE, to_field="id")
    post = ForeignKeyField("models.Post", related_name="models.userPost", on_delete=CASCADE, to_field="id")

    class Meta:
        table = "user_post"
        unique_together = ("user", "post")