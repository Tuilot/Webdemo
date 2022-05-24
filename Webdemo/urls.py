"""Webdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.views import static

from Webdemo import settings
from article.views import front_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', front_page, name='front_page'),
    path('account/', include('account.urls')),
    path('resource/', include('resource.urls')),
    path('article/', include('article.urls')),
    path('comment/', include('comment.urls')),
    path('like/', include('like.urls')),
    path('manager/', include('manager.urls')),
    path('discussion/', include('discussion.urls')),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
]
