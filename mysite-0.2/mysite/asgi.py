"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import sys

import django

import os
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from django.core.asgi import get_asgi_application
import mysite.routing
from mysite.consumers import ChatConsumer
print('asgi.py')
django_asgi_app = get_asgi_application()
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
# from django.core.management import execute_from_command_line
# execute_from_command_line(sys.argv)
# django.setup()


websocket_urlpatterns = [
        path('ws/chat/', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
