import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print('fetch')

        last_10_messages = Messages.objects.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(last_10_messages)
        }

        self.send_message(content)

    def new_message(self, data):
        print('\n\n\n\n\n\n\nnew message\n\n\n\n\n\n\n\n')

        author = data['from']
        content = data['message']
        #print('\n\n\n\n\n\n\n', [author], '\n\n\n\n\n\n')

        author_user = get_object_or_404(User, username=author)
        new_message, created = Messages.objects.get_or_create(author=author_user, content=content)

        content = {
            "command": "new_message",
            "message": self.message_to_json(new_message)
        }

        return self.send_chat_message(content)



    def messages_to_json(self, messages):
        results = []

        for message in messages:
            results.append(self.message_to_json(message))

        return results
    
    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
    }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        #message = data['message']

        selected_func = self.commands[data['command']]
        selected_func(self, data)

    def send_chat_message(self, message):

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def send_message(self, message):
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            message
        ))


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(
            message
        ))



# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
