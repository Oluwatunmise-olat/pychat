from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async


@sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddlewarestack:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        # get the header from the scope
        headers = dict(scope["headers"])

        # check if there is an authorization in the header sent
        if b'authorization' in headers:
            # decode since it returns a byte string
            token_keyward, token = headers[b"authorization"].decode().split()
            if token_keyward == 'Bearer':
                # add the associated token user
                scope['user'] = await get_user(token)

        return await self.inner(scope, receive, send)
