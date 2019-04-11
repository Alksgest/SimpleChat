from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, TemplateView
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.reverse import reverse
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

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

    def get_object(self):  
        return get_object_or_404(ChatRoom, id=self.kwargs['pk'])
   

#headers:
#"action": "add user" | "delete user"
#"userID': int

    def put(self, request, *args, **kwargs):
        action = request.data.get('action', None)

        if action == 'add user':
            id = kwargs.get('pk', None)

            userID = request.data.get('userID', -1)
            try:
                user = User.objects.get(id=userID)
                try:
                    chat_room = ChatRoom.objects.get(id=id)
                    if len(chat_room.users.all()) >= 3:
                        return HttpResponseServerError('to many users in chat room')
                    if chat_room in user.chatRooms.all():
                        return HttpResponseServerError('already in chat room')
                    user.chatRooms.add(chat_room)
                    user.save(update_fields=['chatRooms'])
                except:
                    return HttpResponseServerError('invalid chat room id')
            except:
                return HttpResponseServerError('invalid user id')
        elif action == 'delete user':
            pass
        else:
            return HttpResponseServerError('no action')
        
        return Response()     


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
  

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    # def get_object(self):
    #     return self.request.user


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
    
    # def delete(self, request, *args, **kwargs):
    #     pass


class ChatRoomRedirect(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):

        title = request.GET.get('title', '')
        password = request.GET.get('password', '')
        
        if title != '':
            try:
                chatObj = ChatRoom.objects.get(title=title)
            except:
                return HttpResponseServerError('invalid title')
            return HttpResponsePermanentRedirect(f'/api/chatRooms/{chatObj.id}')
        elif password != '':
            try:
                chatObj = ChatRoom.objects.get(password=password)
            except:
                return HttpResponseServerError('invalid password')
            return HttpResponsePermanentRedirect(f'/api/chatRooms/{chatObj.id}')
            
        return HttpResponseServerError('invalid request')





# chat room old

    # def get(self, request, *args, **kwargs):        
    #     try:
    #         return ChatRoom.objects.get(id=kwargs.get('pk'))
    #     except ObjectDoesNotExist:
    #         return HttpResponseNotFound()
        # id = kwargs.get('pk', None)

        # try:
        #     chat_room = ChatRoom.objects.get(id=id)
        # except ObjectDoesNotExist:
        #     return HttpResponseNotFound()

        # serializer = ChatRoomSerializer(chat_room)   
        # return Response(serializer.data)