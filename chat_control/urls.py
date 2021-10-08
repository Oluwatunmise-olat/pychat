from django.urls import path, re_path

from chat_control import views

urlpatterns = [
    path('chat/<int:user_id>/', views.peer_to_peer),
]
