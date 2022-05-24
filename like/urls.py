from django.urls import path

from like import views

urlpatterns = [
    path('article_like/', views.post_article_like, name='article_likes'),
    path('discussion_like/', views.post_discussion_like, name='discussion_likes'),
]
