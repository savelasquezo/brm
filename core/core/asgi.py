"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from apps.item.routing import websocket_urlpatterns as item_websocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
application = get_asgi_application()

async_websocket_urlpatterns = (item_websocket)

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(async_websocket_urlpatterns))
        ),
    }
)
