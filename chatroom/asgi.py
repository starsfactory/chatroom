"""
ASGI config for chatroom project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from . import routings
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatroom.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(routings.websocket_urlpatterns),
})