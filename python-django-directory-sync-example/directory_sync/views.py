import os
import workos
from django.conf import settings
from django.shortcuts import render


workos.api_key = os.getenv('WORKOS_API_KEY')
workos.base_api_url = 'http://localhost:8000/' if settings.DEBUG else workos.base_api_url
directory_id = os.getenv('DIRECTORY_ID')  # Follow the WorkOS guide to get this

def get_home(request):
    print('request', request)
    return render(request, 'directory_sync/home.html')

def get_directory_users(request):
    users = workos.client.directory_sync.list_users(directory=directory_id)
    return render(request, 'directory_sync/users.html', {"users": users})


def get_directory_groups(request):
    groups = workos.client.directory_sync.list_groups(directory=directory_id)
    return render(request, 'directory_sync/groups.html', {"groups": groups})
