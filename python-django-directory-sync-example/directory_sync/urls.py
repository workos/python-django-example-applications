from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home, name='home'),
    path('users', views.get_directory_users, name='users'),
    path('groups', views.get_directory_groups, name='groups'),
]
