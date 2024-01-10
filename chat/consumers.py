
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    

    async def fetch_messages(self,data):
        messages = Message.objects.filter(room_name=data['room_name']).order_by('-time_stamp').all()[:10]
        content = {
            'messages' : self.messages_to_json(messages)
        }
        self.send_message(content)


    async def new_message(self,data):
        author = data['from']
        author_user = await sync_to_async(User.objects.get)(username=author)

        # Create the message
        message = await sync_to_async(Message.objects.create)(
            author=author_user,
            content=data['message'],
            room_name = data['room_name']
        )

        content = {
            'command': 'new_message',
            'message': await self.message_to_json(message)
        }

        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': content
        }
    )
    

    async def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    

    async def message_to_json(self,message):
        return {
            'author': message.author.username,
            'content': message.content,
            'time_stamp' : str(message.time_stamp),

        }

    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }



    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self,data)



    async def send_chat_message(self,message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    async def send_message(self,message):
        await self.send(text_data=json.dumps(message))


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))