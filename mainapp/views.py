from enum import Enum

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponsePermanentRedirect,
                         HttpResponseServerError)
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, TemplateView
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from .models import Message, User, ChatRoom
from .permissions import IsOwnerOrReadOnly, IsMember
from .serializers import ChatRoomSerializer, ChatRoomAddUserSerializer, ChatRoomDeleteUserSerializer, UserSerializer, MessageSerializer


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
    permission_classes = (permissions.IsAdminUser, )


class Action(Enum):
    ADD = 1,
    DELETE = 2,
    OTHER = 3,
    ERROR = -1


class ChatRoomDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    permission_classes = (permissions.IsAdminUser, IsMember)

    """
    headers:
    "action": "add" | "delete"
    "userID': int
    """

    def _is_retrieve_request(self):
        action = self.request.data.get('action', '')
        if action == 'add':
            return Action.ADD
        elif action == 'delete':
            return Action.DELETE
        return Action.OTHER

    def get_serializer_class(self):
        res = self._is_retrieve_request()
        if res == Action.ADD:
            return ChatRoomAddUserSerializer
        elif res == Action.DELETE:
            return ChatRoomDeleteUserSerializer
        return ChatRoomSerializer  # mb ChatRoomErrorSerializer

    def get_object(self):
        return get_object_or_404(ChatRoom, id=self.kwargs['pk'])

    def get_serializer_context(self):
        return {'request': self.request}


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MessageDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsOwnerOrReadOnly, )


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
