from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class messages_consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    def disconnect(self):
        pass
    