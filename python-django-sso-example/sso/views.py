import os
from workos import WorkOSClient
import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# BASE_DIR is the project root (where manage.py is located)
# views.py is at: python-django-sso-example/sso/views.py
# So we need to go up 2 levels to get to python-django-sso-example/
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path, override=False)  # Don't override existing env vars


# Initialize WorkOS client
# Note: In SDK v5+, we use WorkOSClient instance instead of workos.client module
def get_workos_client():
    """Get WorkOS client instance (initialized lazily)"""
    if not hasattr(get_workos_client, '_instance'):
        # Reload .env file in case it wasn't loaded at import time
        load_dotenv(env_path, override=False)
        
        api_key = os.getenv("WORKOS_API_KEY")
        client_id = os.getenv("WORKOS_CLIENT_ID")
        if not api_key or not client_id:
            raise ValueError(
                "WorkOS API key and client ID must be set via WORKOS_API_KEY and WORKOS_CLIENT_ID environment variables. "
                "Please check your .env file or export these variables."
            )
        get_workos_client._instance = WorkOSClient(
            api_key=api_key,
            client_id=client_id
        )
    return get_workos_client._instance

# For compatibility with other examples, create workos_client variable
# Initialize it if env vars are available, otherwise it will be created on first use
try:
    if os.getenv("WORKOS_API_KEY") and os.getenv("WORKOS_CLIENT_ID"):
        workos_client = WorkOSClient(
            api_key=os.getenv("WORKOS_API_KEY"),
            client_id=os.getenv("WORKOS_CLIENT_ID")
        )
    else:
        workos_client = None
except ValueError:
    # If env vars aren't set at import time, use lazy initialization
    workos_client = None

# Set custom API base URL for local development
if settings.DEBUG:
    os.environ["WORKOS_API_BASE_URL"] = "http://localhost:8000/"

# Constants
CUSTOMER_ORGANIZATION_ID = os.getenv("CUSTOMER_ORGANIZATION_ID")
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
    if not REDIRECT_URI:
        return render(
            request,
            "sso/login.html",
            {"error": "configuration_error", "error_description": "REDIRECT_URI is not configured"},
        )

    login_type = request.POST.get("login_method")
    if not login_type:
        return render(
            request,
            "sso/login.html",
            {"error": "missing_login_method", "error_description": "Login method is required"},
        )

    params = {"redirect_uri": REDIRECT_URI, "state": {}}

    if login_type == "saml":
        if not CUSTOMER_ORGANIZATION_ID:
            return render(
                request,
                "sso/login.html",
                {"error": "configuration_error", "error_description": "CUSTOMER_ORGANIZATION_ID is not configured"},
            )
        params["organization_id"] = CUSTOMER_ORGANIZATION_ID
    else:
        params["provider"] = login_type

    client = workos_client if workos_client else get_workos_client()
    authorization_url = client.sso.get_authorization_url(**params)

    return redirect(authorization_url)


def auth_callback(request):
    # Check for error response from WorkOS
    if "error" in request.GET:
        error = request.GET.get("error")
        error_description = request.GET.get("error_description", "An error occurred during authentication")
        # Log the error and redirect back to login with error message
        return render(
            request,
            "sso/login.html",
            {"error": error, "error_description": error_description},
        )
    
    # Get the authorization code
    code = request.GET.get("code")
    if not code:
        return render(
            request,
            "sso/login.html",
            {"error": "missing_code", "error_description": "No authorization code received"},
        )
    
    try:
        client = workos_client if workos_client else get_workos_client()
        profile = client.sso.get_profile_and_token(code)
        # In SDK v5+, ProfileAndToken is a Pydantic model - use .dict() to convert to dict
        p_profile = profile.dict()
        request.session["p_profile"] = p_profile
        request.session["first_name"] = p_profile["profile"]["first_name"]
        request.session["raw_profile"] = p_profile["profile"]
        request.session["session_active"] = True
        return redirect("login")
    except Exception as e:
        return render(
            request,
            "sso/login.html",
            {"error": "authentication_error", "error_description": str(e)},
        )


def logout(request):
    request.session.clear()
    return redirect("login")
