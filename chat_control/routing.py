from django.urls import re_path, path
from chat_control import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<user_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<int:user_id>/', consumers.ChatConsumer.as_asgi()),
]
