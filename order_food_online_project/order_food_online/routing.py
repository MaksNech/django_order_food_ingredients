from django.urls import include, path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from foods.token_auth import TokenAuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from foods.consumers import CommentAddConsumer, UpdateDishListConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddlewareStack(
            URLRouter(
                [
                 path('foods/dish/view/<slug:dish_slug>/', CommentAddConsumer),
                 path('foods/dish/', UpdateDishListConsumer),
                ]
            )

        )
    )

})