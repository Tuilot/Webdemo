from django.db import models

# Create your models here.
from account.models import Account
from article.models import Article
from discussion.models import Discussion


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.BooleanField(default=0)

    class Meta:
        abstract: True


class ArticleLike(Like):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class DiscussionLike(Like):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
