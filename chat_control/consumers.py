import asyncio
import json
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from chat_control.models import Threads, Message
from channels.db import database_sync_to_async

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self, user):
        return User.objects.get(username=user)

    @database_sync_to_async
    def get_or_create_threads(self, me, other_user):
        thread_instance = Threads.objects.filter(
            Q(me=me) &
            Q(recipient=other_user) |
            Q(me=other_user) &
            Q(recipient=me)
        )
        if not thread_instance.exists():
            thread_instance = Threads.objects.create(
                me=me, recipient=other_user
            )
            return thread_instance
        else:
            return thread_instance.first()

    @database_sync_to_async
    def create_message(self, **kwargs):
        return Message.objects.create(**kwargs)

    @database_sync_to_async
    def get_message_history(self, thread):
        thread_instance = Message.objects.filter(thread=thread)
        if thread_instance.exists():
            return thread_instance.first()
        else:
            return "Why not start a conversation now"

    async def connect(self):
        self.other_user = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'broadcast'
        me = self.scope["user"]
        me = await self.get_user(me)
        self.sender = me
        other_user = await self.get_user(self.other_user)
        self.recipient = other_user
        self.room = await self.get_or_create_threads(me, other_user)
        self.room_group_name = f"personal{self.room.id}"
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # save message to db
        create_message_in_db = await self.create_message(
            thread=self.room, sender=self.sender, recipient=self.recipient, content=message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))
