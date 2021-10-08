from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from user_control.serializers import RegisterSerializer

User = get_user_model()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # get the token of the user and delete it
        currentToken = Token.objects.filter(user=request.user)
        if currentToken.exists():
            currentToken.get().delete()

        logout(request)
        return Response({"status": "success", "message": "Successfully logged out"}, status="200")


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response({'status': True, 'message': "User created successfully"}, status="201")
