from django.urls import path, re_path
from manager.views import article_manager, delete_article, resource_manager, delete_resource, discussion_manager, \
    delete_discussion

urlpatterns = [
    path('article_manager', article_manager, name='article_manager'),
    path('delete_article', delete_article, name='delete_article'),
    path('resource_manager', resource_manager, name='resource_manager'),
    path('delete_resource', delete_resource, name='delete_resource'),
    path('discussion_manager', discussion_manager, name='discussion_manager'),
    path('discussion_resource', delete_discussion, name='delete_discussion'),
]