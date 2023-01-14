import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'notification_%s' % self.room_name
        
        # join to group
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
            )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        
        # leave group
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
            )
        
    # Receive message from websocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]
        
    #     event = {
    #         'type': 'send_message',
    #         'message': message
    #     }
        
    #     # Send message to group
    #     await self.channel_layer.group_send(
    #         self.group_name, 
    #         event
    #         )
        
    # Receive message from group
    async def send_notification(self, event):
        message = json.loads(event['message'])

        # Send message to websocket
        await self.send(text_data=json.dumps(message))
        
        
class RealtimeConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'realtime_%s' % self.room_name
        # join to group
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
            )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        
        # leave group
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
            )
        
    # Receive message from group
    async def send_realtime(self, event):
        message = json.loads(event['message'])
        
        # Send message to websocket
        await self.send(text_data=json.dumps(message))