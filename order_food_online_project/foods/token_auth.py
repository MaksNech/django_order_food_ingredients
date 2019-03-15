from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):

        try:
            token_name, token_key = scope['query_string'].decode().split('=')
            if token_name == 'token':
                token = Token.objects.get(key=token_key)
                scope['user'] = token.user
        except Token.DoesNotExist:
            scope['user'] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
