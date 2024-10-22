from channels.generic.websocket import AsyncWebsocketConsumer
import json
class RoverPositionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'bulbstate'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message': 'Received data'
        }))

    async def send_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
