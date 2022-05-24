from django.urls import path

from account import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('edit/', views.edit_user_info, name='edit_user_info'),
    path('profile/<str:user_id>', views.user_show_info, name='user_show_info'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),
]
