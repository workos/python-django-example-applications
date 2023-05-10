from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "provision_enterprise/", views.provision_enterprise, name="provision_enterprise"
    ),
    path("launch_admin_portal/", views.launch_admin_portal, name="launch_admin_portal"),
]
