import os
from chatapp.channels_interceptor import TokenAuthMiddlewarestack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat_control import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddlewarestack(
        URLRouter(
            routing.websocket_urlpatterns,
        )
    )
})
