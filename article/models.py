from django.db import models
from mdeditor.fields import MDTextField

# Create your models here.
from account.models import Account


class Article(models.Model):
    ChoiceFileType = (
        ('c', 'c++'),
        ('java', 'java'),
        ('golang', 'golang'),
        ('database', '数据库'),
        ('linux', 'linux'),
    )
    id = models.CharField(max_length=30,primary_key=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100,default='标题')
    type = models.CharField(max_length=300, default='', choices=ChoiceFileType)
    content = MDTextField()
    last_update_time = models.DateTimeField(auto_now=True)
    release_time = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
