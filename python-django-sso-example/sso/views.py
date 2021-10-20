import os
import workos
from django.conf import settings
from django.shortcuts import redirect, render


workos.api_key = os.getenv('WORKOS_API_KEY')
workos.client_id = os.getenv('WORKOS_CLIENT_ID')

# In workos_django/settings.py, you can use DEBUG=True for local development,
# but you must use DEBUG=False in order to test the full authentication flow
# with the WorkOS API.
workos.base_api_url = 'http://localhost:8000/' if settings.DEBUG else workos.base_api_url

# Constants
# Required: Fill in either domain or customer_ID or both, at least one must be populated to generate auth connection.
# For testing purposes we fitted domain with gmail.com as an example, please edit and add domains as needed for your testing.
CUSTOMER_EMAIL_DOMAIN = 'gmail.com'
CONNECTION_ID = ''
REDIRECT_URI = os.getenv('REDIRECT_URI')


def login(request):
    return render(request, 'sso/login.html')


def auth(request):

    authorization_url = workos.client.sso.get_authorization_url(
        domain = CUSTOMER_EMAIL_DOMAIN,
        redirect_uri= REDIRECT_URI,
        state={},
        connection= CONNECTION_ID
    )
    return redirect(authorization_url)


def auth_callback(request):
    code = request.GET['code']
    profile = workos.client.sso.get_profile_and_token(code)
    p_profile = profile.to_dict()
    print(p_profile)
    first_name = p_profile['profile']['first_name']

    if "picture" in p_profile['profile']['raw_attributes']:
        image = p_profile['profile']['raw_attributes']['picture']
    else: 
        image = "../static/images/workos_logo.png"

    raw_profile = p_profile['profile']

    return render(request, 'sso/login_successful.html', {
        "p_profile": p_profile,
        "first_name": first_name,
        "image": image,
        "raw_profile": raw_profile
    })
