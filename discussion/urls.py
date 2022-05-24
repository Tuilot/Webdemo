from django.urls import path

from discussion.views import discussion_list, Edit, discussion_detail

urlpatterns = [
    # path('', front_page, name='front_page'),
    path('list', discussion_list, name='discussion_list'),
    path('edit', Edit.as_view(), name='discussion_edit'),
    path('<str:discussion_id>', discussion_detail, name='discussion_detail')
]