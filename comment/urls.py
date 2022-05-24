
from django.urls import path

from comment import views

urlpatterns = [
    path('post_article_comment/', views.post_article_comment, name="post_article_comment"),
    path('post_article_reply_comment/', views.post_article_reply, name="post_article_reply_comment"),
    path('post_discussion_comment/', views.post_discussion_comment, name="post_discussion_comment"),
    path('post_discussion_reply_comment/', views.post_discussion_reply, name="post_discussion_reply_comment"),
]
