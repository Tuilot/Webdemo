from django.urls import path
from resource.views import resource_list, resource_upload

urlpatterns = [
    path('', resource_list, name='resource'),
    path('list/', resource_list, name='resource_list'),
    path('upload/', resource_upload, name='resource_upload'),
    # path('list/', resource_list_views.more, name='resource_more')
]
