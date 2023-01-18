import os
import workos
import json
from django.conf import settings
from django.shortcuts import redirect, render
from datetime import datetime, timedelta

from audit_logs.audit_log_events import (
    user_signed_in,
    user_logged_out,
    user_connection_deleted,
    user_organization_deleted,
    user_organization_set,
)
from django.views.decorators.csrf import csrf_exempt

workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")

# In workos_django/settings.py, you can use DEBUG=True for local development,
# but you must use DEBUG=False in order to test the full authentication flow
# with the WorkOS API.
workos.base_api_url = (
    "http://localhost:8000/" if settings.DEBUG else workos.base_api_url
)

# Constants
# Required: Fill in CONNECTION_ID for the desired connection from the WorkOS Dashboard

REDIRECT_URI = os.getenv("REDIRECT_URI")


def login(request):
    if request.session.get("session_active") == None:
        before = request.GET.get("before")
        after = request.GET.get("after")
        organizations = workos.client.organizations.list_organizations(
            limit=5, before=before, after=after
        )
        before = organizations["listMetadata"]["before"]
        after = organizations["listMetadata"]["after"]
        organizations = organizations["data"]
        return render(
            request,
            "audit_logs/login.html",
            {"organizations": organizations, "before": before, "after": after},
        )

    if request.session.get("session_active") == True:
        return render(
            request,
            "audit_logs/send_events.html",
            {
                "org_name": request.session.get("organization_name"),
                "organization_id": request.session.get("organization_id"),
            },
        )


@csrf_exempt
def set_org(request):
    organization_id = request.GET["id"]
    request.session["organization_id"] = organization_id
    organization_set = workos.client.audit_logs.create_event(
        organization_id, user_organization_set
    )
    org = workos.client.organizations.get_organization(organization_id)
    org_name = org["name"]
    request.session["organization_name"] = org_name
    request.session["session_active"] = True
    return redirect("login")


@csrf_exempt
def send_event(request):
    event_type = request.POST["event"]
    organization_id = request.session["organization_id"]
    events = [
        user_signed_in,
        user_logged_out,
        user_organization_deleted,
        user_connection_deleted,
    ]
    event = events[int(event_type)]
    organization_set = workos.client.audit_logs.create_event(organization_id, event)
    return redirect("login")


@csrf_exempt
def export_events(request):
    return render(
        request,
        "audit_logs/export_events.html",
        {
            "org_name": request.session.get("organization_name"),
            "organization_id": request.session.get("organization_id"),
        },
    )


@csrf_exempt
def get_events(request):
    organization_id = request.session.get("organization_id")
    event_type = request.POST["event"]

    today = datetime.today()
    last_month = today - timedelta(days=30)
    last_month_iso = last_month.isoformat()
    today_iso = today.isoformat()

    if event_type == "generate_csv":
        create_export_response = workos.client.audit_logs.create_export(
            organization=organization_id,
            range_start=last_month_iso,
            range_end=today_iso,
        )
        request.session["export_id"] = create_export_response.to_dict()["id"]

    if event_type == "access_csv":
        export_id = request.session.get("export_id")
        fetch_export_response = workos.client.audit_logs.get_export(export_id)
        return redirect(fetch_export_response.to_dict()["url"])

    return redirect("export_events")


def logout(request):
    request.session.clear()
    return redirect("login")
