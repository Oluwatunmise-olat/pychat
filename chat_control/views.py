from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Q

from chat_control.models import Threads, Message
from chat_control.serializers import PreviousMessageSerializer

User = get_user_model()


@api_view(['GET'])
def peer_to_peer(request, user_channel_name):
    serializer_class = PreviousMessageSerializer
    """
        This function handles loading of
        previous chat of users.
        Note: It is a peer to peer system
    """
    me = User.objects.get(username=request.user.username)
    other_user = User.objects.get(username=user_channel_name)
    thread_instance = Threads.objects.filter(
        Q(me=me) &
        Q(recipient=other_user) |
        Q(me=other_user) &
        Q(recipient=me)
    )
    if not thread_instance.exists():
        return Response({'chat_history': []}, status="200")

    history = Message.objects.filter(thread=thread_instance.first())
    previous_chat = serializer_class(history, many=True).data
    return Response({'chat_history': previous_chat.data}, status="200")
