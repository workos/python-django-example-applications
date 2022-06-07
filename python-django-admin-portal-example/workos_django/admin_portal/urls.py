from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "provision_enterprise/", views.provision_enterprise, name="provision_enterprise"
    ),
    path("sso_admin_portal/", views.sso_admin_portal, name="sso_admin_portal"),
    path("dsync_admin_portal/", views.dsync_admin_portal, name="dsync_admin_portal"),
]
