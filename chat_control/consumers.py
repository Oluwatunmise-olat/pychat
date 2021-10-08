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

user_1 = User.objects.get(id=1).id
user_2 = User.objects.get(id=3).id


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_user(self, user_id: int):
        return User.objects.get(id=user_id)

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
        print(self.scope['user'], "*finally*****")
        self.other_user = self.scope['url_route']['kwargs']['user_id']
        me = self.scope["user"]
        me = await self.get_user(me.id)
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
        print("disconnect *********")
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
                'message': message,
                'sender': create_message_in_db.sender,
                'recipient': create_message_in_db.recipient
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print(event, "mooo")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': event['sender'].id,
            'sender_name': event['sender'].username,
            'recipient_name': event['recipient'].username,
            'recipient_id': event['recipient'].id
        }))
