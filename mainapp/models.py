from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime

class ChatRoom(models.Model):
    title = models.CharField(verbose_name='Title', max_length=30, unique=True)
    password = models.CharField(verbose_name='Password', max_length=24, default='sfxf432')
  

class User(AbstractUser):
    chatRooms = models.ManyToManyField(ChatRoom, related_name='users') # , through='UserChatRoomMembership'
    #chatRoom = models.ForeignKey(ChatRoom, verbose_name='ChatRoom', related_name='users', on_delete=models.)

class Message(models.Model):
    message = models.TextField(verbose_name='Message')
    date = models.DateTimeField(verbose_name='Date', default=datetime.datetime.now()) #auto_now_add=True, blank=True
    owner = models.ForeignKey(User, default=1, verbose_name="Owner", on_delete=models.CASCADE, related_name="messages")
    chatRoom = models.ForeignKey(ChatRoom, default=1, related_name='messages', on_delete=models.CASCADE, verbose_name="ChatRoom")
     #chatRoom = models.OneToOneField(ChatRoom, default=None, on_delete=models.CASCADE, null=True)

# class UserChatRoomMembership(models.Model):
#     chatRoom = models.ForeignKey(ChatRoom, verbose_name="Chat room", on_delete=models.CASCADE)
#     user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    

    
