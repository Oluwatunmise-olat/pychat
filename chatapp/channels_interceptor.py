# from django.contrib.auth.models import AnonymousUser
#
# from rest_framework.authtoken.models import Token
#
# from channels.auth import AuthMiddlewareStack
# from channels.db import database_sync_to_async
# from asgiref.sync import sync_to_async
#
#
# @sync_to_async
# def get_user(token):
#     try:
#         token = Token.objects.get(key=token)
#         return token.user
#     except Token.DoesNotExist:
#         return AnonymousUser()
#
#
# class TokenAuthMiddleware:
#     def __init__(self, inner):
#         self.inner = inner
#
#     def __call__(self, scope):
#         return TokenAuthMiddlewareInstance(scope, self)
#
#
# class TokenAuthMiddlewareInstance:
#
#     def __init__(self, scope, middleware):
#         self.middleware = middleware
#         self.scope = dict(scope)
#         self.inner = self.middleware.inner
#
#     async def __call__(self, receive, send):
#
#         # get the header from the scope
#         headers = dict(self.scope["headers"])
#
#         # check if there is an authorization in the header sent
#         if b'authorization' in headers:
#             # decode since it returns a byte string
#             token_keyward, token = headers[b"authorization"].decode().split()
#             if token_keyward == 'Bearer':
#                 # add the associated token user
#                 self.scope['user'] = await get_user(token)
#
#         return self.inner(self.scope, receive, send)
#
#
# def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(AuthMiddlewareStack(inner))


from channels.middleware import BaseMiddleware
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token_key = scope['query_string'].decode().split('=')[-1]

        scope['user'] = await get_user(token_key)

        return await super().__call__(scope, receive, send)
