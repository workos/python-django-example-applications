import os
import json
import workos
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import socketio

from workos_django.settings import BASE_DIR

basedir = BASE_DIR
sio = socketio.Server()
thread = None

workos.api_key = os.getenv("WORKOS_API_KEY")
workos.base_api_url = (
    "http://localhost:8000/" if settings.DEBUG else workos.base_api_url
)


def get_home(request):
    before = request.GET.get("before")
    after = request.GET.get("after")
    directories = workos.client.directory_sync.list_directories(
        limit=5, before=before, after=after
    )
    before = directories["listMetadata"]["before"]
    after = directories["listMetadata"]["after"]
    directories = directories["data"]
    return render(
        request,
        "directory_sync/home.html",
        {"directories": directories, "before": before, "after": after},
    )


def get_directory(request):
    directory_id = request.GET["id"]
    directory = workos.client.directory_sync.get_directory(directory_id)
    json_directory = json.dumps(
        workos.client.directory_sync.get_directory(directory_id), indent=2
    )
    return render(
        request,
        "directory_sync/directory.html",
        {
            "directory_id": directory_id,
            "directory": directory,
            "json_directory": json_directory,
        },
    )


def get_directory_users(request):
    directory_id = request.GET["id"]
    users = workos.client.directory_sync.list_users(directory=directory_id, limit=100)
    return render(request, "directory_sync/users.html", {"users": users})


def get_directory_groups(request):
    directory_id = request.GET["id"]
    groups = workos.client.directory_sync.list_groups(directory=directory_id, limit=100)
    print(groups)
    return render(request, "directory_sync/groups.html", {"groups": groups})


@csrf_exempt
def webhooks(request):
    if request.body:
        payload = request.body
        sig_header = request.headers.get("WorkOS-Signature")
        response = workos.client.webhooks.verify_event(
            payload=payload, sig_header=sig_header, secret=os.getenv("WEBHOOKS_SECRET")
        )
        message = json.dumps(response)
        sio.emit("webhook_received", message)

    return render(request, "directory_sync/webhooks.html")
