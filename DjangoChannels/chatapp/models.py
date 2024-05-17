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