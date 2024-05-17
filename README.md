# Django-Channels

## Integrate the Channels library

1. python -m pip install -U channels["daphne"]
2. add **daphne** in installed app
3. in **asgi.py** add those lines 
<pre> import os
    from channels.routing import ProtocolTypeRouter
    from django.core.asgi import get_asgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django_asgi_app = get_asgi_application()
    application = ProtocolTypeRouter({
        "http": django_asgi_app,
    })</pre>
4. Replace `my site` with your project name
5. add this line in ur project settings <pre>ASGI_APPLICATION = "myproject.asgi.application"</pre>
6. Download Redis [Download Redis](https://github.com/microsoftarchive/redis/releases/tag/win-2.8.2104)
7. Run `redis-server.exe`
8. Add channel layer in your settings
<pre>
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }
</pre>
9. Congratulation ur django channels all set :)
### [A very simple explanation of the difference between ASGI and WSGI](https://github.com/prackels/Tutorials/blob/main/asgi%20%26%20wsgi.md)

# Creating first project with channels (Chat App)
1. Create new app `chatapp`
2. Create `chatapp/models` <pre>
    from django.db import models
    from django.contrib.auth import get_user_model
    user= get_user_model()
    class Room(models.Model):
        name = models.CharField(max_length=255, unique=True)

    class Message(models.Model):
        room = models.ForeignKey(Room, on_delete=models.CASCADE)
        user = models.ForeignKey(user, on_delete=models.CASCADE)
        text = models.TextField()
        message_time = models.DateTimeField(auto_now_add=True)
    </pre>
3. create `chatapp/consumers.py` <pre>
    import json
    from asgiref.sync import async_to_sync
    from channels.generic.websocket import WebsocketConsumer
    from chat_models.models import Room, Message

    class ChatConsumer(WebsocketConsumer):
        def connect(self, room_name):
            self.room_name = room_name
            self.room_group_name = f'chat_{room_name}'
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            self.accept()

        def receive(self, text_data):
            data = json.loads(text_data)
            message = data['message']
            message_obj = Message.objects.create(
                room=Room.objects.get(name=self.room_name),
                user=self.scope['user'],
                text=message
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_obj.text,
                    'username': message_obj.user.username
                }
            )
        def disconnect(self, message):
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
</pre> 

#### routing like urls.py
4. Create `chatapp/routing.py` <pre>from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatConsumer
channel_routing = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    ]),
})</pre>