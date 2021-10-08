from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


class TokenAuth:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # channels states that a callable be returned

        # get the header from the scope
        headers = dict(scope["headers"])

        # check if there is an authorization in the header sent
        if 'Authorization' in headers:
            # decode since it returns a byte string
            token_keyward, token = headers["Authorization"].decode().split()
            if token_keyward == 'Bearer':
                try:
                    token_valid = Token.objects.get(key=token)
                except Token.DoesNotExist:
                    scope['user'] = AnonymousUser()
                else:
                    # add the associated token user
                    scope['user'] = token_valid.user

        return self.inner(scope)
