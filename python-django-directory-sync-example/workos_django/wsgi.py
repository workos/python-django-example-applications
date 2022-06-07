"""
WSGI config for workos_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workos_django.settings")

from socketio import WSGIApp
from directory_sync.views import sio


directory_sync = StaticFilesHandler(get_wsgi_application())

application = WSGIApp(sio, directory_sync)

import eventlet
import eventlet.wsgi

eventlet.wsgi.server(eventlet.listen(("", 8000)), application)
