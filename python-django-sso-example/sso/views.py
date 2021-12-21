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

CONNECTION_ID = 'xxx'
REDIRECT_URI = os.getenv('REDIRECT_URI')


def login(request):
    print(request.session.get('session_active'))
    if request.session.get('session_active') == None:
        return render(request, 'sso/login.html')

    if request.session.get('session_active') == True:
        print('this is the session', request.session)
        return render(request, 'sso/login_successful.html', {
            "p_profile": request.session.get('p_profile'),
            "first_name": request.session.get('first_name'),
            "raw_profile": request.session.get('raw_profile')
        })

    
def auth(request):
    authorization_url = workos.client.sso.get_authorization_url(
        connection= CONNECTION_ID,
        redirect_uri= REDIRECT_URI,
        state={},        
    )
    return redirect(authorization_url)


def auth_callback(request):
    code = request.GET['code']
    profile = workos.client.sso.get_profile_and_token(code)
    p_profile = profile.to_dict()
    request.session['p_profile'] = p_profile
    request.session['first_name'] = p_profile['profile']['first_name']
    request.session['raw_profile'] = p_profile['profile']
    request.session['session_active'] = True
    return redirect('login')
    
def logout(request):
    request.session.clear()
    return redirect('login')
