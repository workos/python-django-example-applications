from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("passwordless_auth/", views.passwordless_auth, name="passwordless_auth"),
    path("success/", views.success, name="success"),
]
