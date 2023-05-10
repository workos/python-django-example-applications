from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import os
import workos
from workos import client as workos_client
from workos import portal


workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")

# In workos_django/settings.py, you can use DEBUG=True for local development,
# but you must use DEBUG=False in order to test the full authentication flow
# with the WorkOS API.

workos.base_api_url = (
    "http://localhost:8000/" if settings.DEBUG else workos.base_api_url
)


def index(request):
    return render(request, "admin_portal/index.html")


def provision_enterprise(request):
    # Create global variable for org_id
    global org_id

    # retrieve and set variables for the organiation and domains
    organization_name = request.POST["org"]
    organization = request.POST["domain"]

    # use split to modify the domains in to a list type
    organization_domains = organization.split()

    # Check if a matching domain already exists and set global org_id if there is a match
    orgs = orgs = workos_client.organizations.list_organizations(
        domains=organization_domains
    )
    if len(orgs["data"]) > 0:
        org_id = orgs["data"][0]["id"]

    # Otherwise create a new Organization and set the global org_id
    else:
        organization = workos_client.organizations.create_organization(
            {"name": organization_name, "domains": organization_domains}
        )
        org_id = organization["id"]

    return render(request, "admin_portal/org_logged_in.html")


def launch_admin_portal(request):
    intent = request.GET.get("intent")
    portal_link = workos_client.portal.generate_link(organization=org_id, intent=intent)
    return redirect(portal_link["link"])
