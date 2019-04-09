from rest_framework import serializers

from .models import ChatRoom, Message, User

class ChatRoomSerializer(serializers.ModelSerializer):
    #messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all())
    messages_ids = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('id', 'title', 'messages_ids', 'users')
        
    def get_messages_ids(self, chatRoom):
        queryset = Message.objects.filter(chatRoom_id=chatRoom.id)
        return queryset
    

    def get_users(self, chatRoom):
        queryset = Message.objects.filter(chatRoom_id=chatRoom.id)
        return queryset


class UserSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'chatRooms', 'messages')

    def get_messages(self, user):
        queryset = Message.objects.filter(owner_id=user.id)
        return queryset


class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    chatRoom = serializers.ReadOnlyField(source='chatToom.title')
    # owner = UserSerializer
    # ChatRoom = ChatRoomSerializer

    class Meta:
        model = Message
        fields = ('id', 'message', 'date', 'owner', 'chatRoom')

