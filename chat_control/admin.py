from django.contrib import admin

from chat_control.models import Threads, Message

admin.site.register((Threads, Message))
