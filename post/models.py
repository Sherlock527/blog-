from django.db import models

# Create your models here.

from user.models import User


class Post(models.Model):
    class Meta:
        db_table='post'

    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=256,null=False)
    postdate=models.DateTimeField(null=False)
    # 指定外键，migrate会生成author_id字段
    author=models.ForeignKey(User)
    # self.content可以访问Content实例，其内容是self.content.content

    def __repr__(self):
        return '<Post id={} title={} author_id={} content={}>'.format(self.id,self.title,self.author_id, self.content)

    __str__=__repr__


class Content(models.Model):
    class Meta:
        db_table='content'

    # 没有主键，会自动创建一个自增主键
    # 一对一，这边会有一个外键post_id引用自post.id
    post=models.OneToOneField(Post)
    content=models.TextField(null=False)

    def __repr__(self):
        return '<Content id={} content={} >'.format(self.post.id,self.content[:20])

    __str__ = __repr__

