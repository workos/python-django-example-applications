from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_home, name="home"),
    path("directory", views.get_directory, name="directory"),
    path("users", views.get_directory_users, name="users"),
    path("groups", views.get_directory_groups, name="groups"),
    path("webhooks", views.webhooks, name="webhooks"),
]
