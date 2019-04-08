from rest_framework import serializers

from .models import *


class ChatRoomSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all())
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.get(""" get users for this chat room """))

    class Meta:
        model = ChatRoom
        fields = ('id', 'title')

class UserSerializer(serializers.ModelSerializer):
    chatRooms = serializers.PrimaryKeyRelatedField(many=True, queryset=ChatRoom.objects.get(""" get chatrooms for this user """))
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.get(""" get messages for this user """))

    class Meta:
        model = User
        fields = ('id', 'username', 'chatRooms')

class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    chatRoom = serializers.ReadOnlyField(source='chatToom.title')

    class Meta:
        model = Message
        fields = ('id', 'message', 'date', 'owner', 'chatRoom')
