"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

settings_module = ("backend.deploy_settings" if "RENDER_EXTERNAL_HOSTNAME" in os.environ else "backend.settings")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = ProtocolTypeRouter (
    {
        'http' : get_asgi_application(),
        'websocket' : AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),  
    }
)