import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
import base64
from django.conf import settings

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        print(self.chat_id)
        self.room_group_name = f"chat_{self.chat_id}"

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
        from .models import Chat, Message
        from user.models import CustomUser
        
        data = json.loads(text_data)
        print("Receive from websocket:", data)

        message_content = data.get('content', '')
        author_email = data.get('author')
        image_data = data.get('image', None)
        # print(image_data)

        try:
            if image_data:
                image_format, imagestr = image_data.split(';base64,')
                ext = image_format.split('/')[-1]

                img = ContentFile(base64.b64decode(imagestr), name=f'chat_image_{self.chat_id}.{ext}')
            
            else:
                img = None

            chat = await Chat.objects.aget(id=self.chat_id) 
            author = await CustomUser.objects.aget(email=author_email)
            message = await Message.objects.acreate(chat=chat, author=author, content=message_content, image=img)
            print("Image URL being sent:", )


            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'content': message.content,
                    'image': f'{message.image.url}' if message.image else None,
                    'author': author.email,
                    'created_at': message.created_at.isoformat(),
                }
            )
            
        except Chat.DoesNotExist:
            print(f"Chat with ID {self.chat_id} does not exist.")
        except CustomUser.DoesNotExist:
            print(f"User with ID {author_email} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    async def chat_message(self, event):
        print('Event: ', event)
        await self.send(text_data=json.dumps(
            {
                'content' : event['content'],
                'image': event.get('image'),
                'author' : event['author'],
                'created_at' : event['created_at']
            }
        ))