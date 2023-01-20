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


def index(request):
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
            "audit_logs/index.html",
            {"organizations": organizations, "before": before, "after": after},
        )

    if request.session.get("session_active") == True:
        today = datetime.today()
        last_month = today - timedelta(days=30)
        return render(
            request,
            "audit_logs/send_events.html",
            {
                "org_name": request.session.get("organization_name"),
                "organization_id": request.session.get("organization_id"),
                "last_month_iso": last_month.isoformat(),
                "today_iso": today.isoformat(),
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
    return redirect("index")


@csrf_exempt
def send_event(request):
    event_version, actor_name, actor_type, target_name, target_type = (
        request.POST["event-version"],
        request.POST["actor-name"],
        request.POST["actor-type"],
        request.POST["target-name"],
        request.POST["target-type"],
    )
    organization_id = request.session["organization_id"]

    event = {
        "action": "user.organization_deleted",
        "version": int(event_version),
        "occurred_at": datetime.now().isoformat(),
        "actor": {
            "type": actor_type,
            "name": actor_name,
            "id": "user_01GBNJC3MX9ZZJW1FSTF4C5938",
        },
        "targets": [
            {
                "type": target_type,
                "name": target_name,
                "id": "team_01GBNJD4MKHVKJGEWK42JNMBGS",
            },
        ],
        "context": {
            "location": "123.123.123.123",
            "user_agent": "Chrome/104.0.0.0",
        },
    }
    organization_set = workos.client.audit_logs.create_event(organization_id, event)
    return redirect("index")


@csrf_exempt
def export_events(request):
    today = datetime.today()
    last_month = today - timedelta(days=30)

    return render(
        request,
        "audit_logs/send_events.html",
        {
            "org_name": request.session.get("organization_name"),
            "organization_id": request.session["organization_id"],
            "last_month_iso": last_month.isoformat(),
            "today_iso": today.isoformat(),
        },
    )


@csrf_exempt
def get_events(request):
    organization_id = request.session.get("organization_id")
    event_type = request.POST["event"]

    if event_type == "generate_csv":
        if request.POST["filter-actions"] != "":
            actions = request.POST["filter-actions"]
        else:
            actions = None
        if request.POST["filter-actors"] != "":
            actors = request.POST["filter-actors"]
        else:
            actors = None
        if request.POST["filter-targets"] != "":
            targets = request.POST["filter-targets"]
        else:
            targets = None

        try:
            create_export_response = workos.client.audit_logs.create_export(
                organization=organization_id,
                range_start=request.POST["range-start"],
                range_end=request.POST["range-end"],
                actions=actions,
                actors=actors,
                targets=targets,
            )
            request.session["export_id"] = create_export_response.to_dict()["id"]

            return redirect("export_events")
        except Exception as e:
            print(str(e))
            return redirect("/")
    if event_type == "access_csv":
        export_id = request.session["export_id"]
        fetch_export_response = workos.client.audit_logs.get_export(export_id)
        return redirect(fetch_export_response.to_dict()["url"])


@csrf_exempt
def events(request):
    link = workos.client.portal.generate_link(
        organization=request.session["organization_id"], intent="audit_logs"
    )
    return redirect(link["link"])


def logout(request):
    request.session.clear()
    return redirect("index")
