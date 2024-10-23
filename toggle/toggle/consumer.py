from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


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
        await self.save_data(data)
        await self.send(text_data=json.dumps({
            'message': 'Data saved successfully'
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'bulbstate',
                'data': data
            }
        )


    async def send_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def save_data(self, data):
        # Convert data to the format required by the model
        sensor_data = {
            'voltage': data.get('voltage'),
            'current': data.get('current'),
        }
        print(data)

        # Use DRF serializer to validate and save
       