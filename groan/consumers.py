import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        player_name = self.scope['url_route']['kwargs']['player_name']
        self.room_name = room_name.replace(' ', '-')
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("Received message: {}".format(text_data))
        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            text_data_json
        )
