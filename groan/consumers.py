import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Avg

from groan.models import Groan


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = room_name.replace(' ', '-')
        self.room_group_name = 'chat_%s' % self.room_name

        self.groan = await self.create_groan()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        avg = await self.remove_groan()
        await self.send_avg_to_group(avg)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("Received message: {}".format(text_data))
        event = json.loads(text_data)
        new_average = await self.update_groan(event)

        await self.send_avg_to_group(new_average)

    async def send_avg_to_group(self, new_average):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "new_average",
                "average": new_average,
            }
        )

    async def new_average(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def create_groan(self):
        g = Groan(magnitude=50)
        g.save()
        return g

    @database_sync_to_async
    def update_groan(self, event):
        value = event['value']
        self.groan.magnitude = value
        self.groan.save()
        return Groan.objects.all().aggregate(Avg('magnitude'))

    @database_sync_to_async
    def remove_groan(self):
        self.groan.delete()
        return Groan.objects.all().aggregate(Avg('magnitude'))
