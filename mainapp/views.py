from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


from .models import *
from .serializers import *
from .permissions import *

from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'chatRooms': reverse('chatroom-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'messages': reverse('message-list', request=request, format=format),
    })



class ChatRoomList(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class ChatRoomDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
  

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsOwner, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
class MessageDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsOwner, )
    
    def delete(self, request, *args, **kwargs):
        pass


class ChatRoomRedirect(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):

        title = request.GET.get('title', '')
        password = request.GET.get('password', '')
        
        if title != '':
            try:
                chatObj = ChatRoom.objects.get(title=title)
            except:
                HttpResponseNotFound()
            return HttpResponsePermanentRedirect(f'/api/chatRooms/{chatObj.id}')
        elif password != '':
            try:
                chatObj = ChatRoom.objects.get(password=password)
            except:
                HttpResponseNotFound()
            return HttpResponsePermanentRedirect(f'/api/chatRooms/{chatObj.id}')
            
        return HttpResponseNotFound()
