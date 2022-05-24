from django.urls import path, re_path
from article.views import article_list, front_page
from article.views import Edit, article_detail

urlpatterns = [
    # path('', front_page, name='front_page'),
    path('list', article_list, name='articlelist'),
    path('edit',Edit.as_view(), name='article_edit'),
    path('<str:article_id>', article_detail, name='article_detail')
]
