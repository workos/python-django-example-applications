import os
import workos
import json
from workos import client as workos_client
from workos import passwordless
from django.conf import settings
from django.shortcuts import redirect, render


workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")

# In workos_django/settings.py, you can use DEBUG=True for local development,
# but you must use DEBUG=False in order to test the full authentication flow
# with the WorkOS API.
workos.base_api_url = (
    "http://localhost:8000/" if settings.DEBUG else workos.base_api_url
)


def login(request):
    return render(request, "magic_link/login.html")


def passwordless_auth(request):
    email = request.POST["email"]
    redirect_uri = "http://localhost:8000/success"
    session = workos_client.passwordless.create_session(
        {"email": email, "type": "MagicLink", "redirect_uri": redirect_uri}
    )
    workos_client.passwordless.send_session(session["id"])

    # Send a custom email using your own service
    print(email, session["link"])

    # Finally, redirect to a "Check your email" page
    return render(
        request,
        "magic_link/serve_magic_link.html",
        {"email": email, "magic_link": session["link"]},
    )


def success(request):
    code = request.GET["code"]
    try:
        profile = workos_client.sso.get_profile_and_token(code)
    except:
        print(profile)
    p_profile = profile.to_dict()
    raw_profile = json.dumps(p_profile["profile"], indent=2)

    return render(request, "magic_link/success.html", {"raw_profile": raw_profile})
