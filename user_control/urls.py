from rest_framework.authtoken import views as token_view
from django.urls import path

from user_control import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', token_view.obtain_auth_token),
    path('logout', views.LogoutView.as_view()),
]
