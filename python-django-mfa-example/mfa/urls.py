from django.urls import path
from . import views


urlpatterns = [
    path("", views.list_factors, name="list_factors"),
    path(
        "enroll_factor_details",
        views.enroll_factor_details,
        name="enroll_factor_details",
    ),
    path("enroll_sms_factor", views.enroll_sms_factor, name="enroll_sms_factor"),
    path("enroll_totp_factor", views.enroll_totp_factor, name="enroll_totp_factor"),
    path("factor_detail", views.factor_detail, name="factor_detail"),
    path("challenge_factor", views.challenge_factor, name="challenge_factor"),
    path("verify_factor", views.verify_factor, name="verify_factor"),
    path("clear_session", views.clear_session, name="clear_session"),
]
