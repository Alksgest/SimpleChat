from django.db import models
from django.contrib.auth.models import AbstractUser

import random

class ChatRoom(models.Model):

    title = models.CharField(verbose_name='Title', max_length=30)
    password = models.CharField(verbose_name='Password', max_length=24, default=str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)))

    def generateRandomPassword(self):
        psw = ''
        for i in range(0, 24):
            psw += str(random.randint(0, 9))
        return psw
      

class User(AbstractUser):
    chatRooms = models.ManyToManyField(ChatRoom)
    #chatRoom = models.ForeignKey(ChatRoom, verbose_name='ChatRoom', related_name='users', on_delete=models.)

class Message(models.Model):
    message = models.TextField(verbose_name='Message')
    date = models.DateTimeField(verbose_name='Date')
    owner = models.ForeignKey(User, default=1, verbose_name="Owner", on_delete=models.CASCADE)
    chatRoom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE, verbose_name="ChatRoom")
     #chatRoom = models.OneToOneField(ChatRoom, default=None, on_delete=models.CASCADE, null=True)
    

    
