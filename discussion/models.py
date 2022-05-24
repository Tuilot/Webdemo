from django.db import models
from mdeditor.fields import MDTextField

from account.models import Account


class Discussion(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=300, default='标题')
    author = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    content = MDTextField()
    last_update_time = models.DateTimeField(auto_now=True)
    release_time = models.DateTimeField(auto_now_add=True)
    article_type = models.CharField(max_length=1000)