from django.urls import path

from chat_control import views

urlpatterns = [
    path('chat/', views.peer_to_peer),
]
