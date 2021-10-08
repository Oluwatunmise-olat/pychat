import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack

# from chatapp.channels_interceptor import TokenAuthMiddlewareStack
from chat_control import routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": TokenAuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns,
#         )
#     )
# })


from channels.security.websocket import AllowedHostsOriginValidator
from chatapp.channels_interceptor import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)))
})
