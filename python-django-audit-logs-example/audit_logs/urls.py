from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("set_org", views.set_org, name="set_org"),
    path("send_event", views.send_event, name="send_event"),
    path("get_events", views.get_events, name="get_events"),
    path("events", views.events, name="events"),
    path("logout", views.logout, name="logout"),
]
