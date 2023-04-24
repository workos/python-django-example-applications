import os
import workos
import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse


workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")

# In workos_django/settings.py, you can use DEBUG=True for local development,
# but you must use DEBUG=False in order to test the full authentication flow
# with the WorkOS API.
workos.base_api_url = (
    "http://localhost:8000/" if settings.DEBUG else workos.base_api_url
)

# Constants
# Required: Fill in CUSTOMER_ORGANIZATION_ID for the desired organization from the WorkOS Dashboard

CUSTOMER_ORGANIZATION_ID = "xxx"
REDIRECT_URI = os.getenv("REDIRECT_URI")


def login(request):
    if request.session.get("session_active") == None:
        return render(request, "sso/login.html")

    if request.session.get("session_active") == True:
        return render(
            request,
            "sso/login_successful.html",
            {
                "p_profile": request.session.get("p_profile"),
                "first_name": request.session.get("first_name"),
                "raw_profile": json.dumps(request.session.get("raw_profile"), indent=2),
            },
        )


def auth(request):

    login_type = request.POST["login_method"]
    params = {"redirect_uri": REDIRECT_URI, "state": {}}

    if login_type == "saml":
        params["organization"] = CUSTOMER_ORGANIZATION_ID
    else:
        params["provider"] = login_type

    authorization_url = workos.client.sso.get_authorization_url(**params)

    return redirect(authorization_url)


def auth_callback(request):
    code = request.GET["code"]
    profile = workos.client.sso.get_profile_and_token(code)
    p_profile = profile.to_dict()
    request.session["p_profile"] = p_profile
    request.session["first_name"] = p_profile["profile"]["first_name"]
    request.session["raw_profile"] = p_profile["profile"]
    request.session["session_active"] = True
    return redirect("login")


def logout(request):
    request.session.clear()
    return redirect("login")
