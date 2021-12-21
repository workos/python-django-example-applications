from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('auth', views.auth, name='auth'),
    path('auth/callback', views.auth_callback, name='auth_callback'),
    path('logout', views.logout, name='logout'),
]
