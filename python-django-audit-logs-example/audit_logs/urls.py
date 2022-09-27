from django.urls import path
from . import views


urlpatterns = [
    path("", views.login, name="login"),
    path("set_org", views.set_org, name="set_org"),
    path("send_event", views.send_event, name="send_event"),
    path("export_events", views.export_events, name="export_events"),
    path("get_events", views.get_events, name="get_events"),
    path("logout", views.logout, name="logout"),
]
