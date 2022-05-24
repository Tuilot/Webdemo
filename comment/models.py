from django.db import models

# Create your models here.
from django.db import models

from account.models import Account
from article.models import Article
from discussion.models import Discussion


class Comment(models.Model):
    commenter = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment_id = models.IntegerField(default=-1)
    reply_user_id = models.IntegerField(default=-1)
    reply_user_name = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    comment_time = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)


class ArticleComment(Comment):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class DiscussionComment(Comment):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)



