import asyncio
import json
from authentication.models import CustomUser
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Dish, Comment


class CommentAddConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })

        dish_id = await self.get_dish_id(self.scope['url_route']['kwargs']['dish_slug'])

        self.dish = 'dish_' + dish_id

        await self.channel_layer.group_add(
            self.dish,
            self.channel_name
        )

    async def websocket_receive(self, event):
        data = event.get('text')
        comment_data = json.loads(data)
        dish_slug = comment_data['dish_slug']
        author_id = comment_data['author_id']
        author_name = CustomUser.objects.get(id=author_id).username
        body = comment_data['body']

        await self.create_comment(dish_slug, body, author_id)

        created_on = str(Comment.objects.get(body=body).created_on.strftime("%Y-%m-%d %H:%M:%S"))

        comment = {
            'body': body,
            'author': author_name,
            'created_on': created_on
        }

        await self.channel_layer.group_send(
            self.dish,
            {
                'type': 'show_comment',
                'text': json.dumps(comment)
            }
        )

    async def websocket_disconnect(self, event):
        pass

    @database_sync_to_async
    def create_comment(self, dish_slug, body, author_id):
        author = CustomUser.objects.get(id=author_id)
        dish = Dish.objects.get(slug=dish_slug)
        Comment.objects.create(dish=dish, body=body, author=author)

    @database_sync_to_async
    def get_dish_id(self, dish_slug):
        return str(Dish.objects.get(slug=dish_slug).id)

    async def show_comment(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
