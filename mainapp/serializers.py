from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import ChatRoom, Message, User

class ChatRoomBaseSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('users', )

    def get_users(self, chatRoom):
        return [item.id for item in chatRoom.users.all()]


class ChatRoomSerializer(ChatRoomBaseSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all())
 
    class Meta:
        model = ChatRoom
        fields = ('id', 'messages', 'users', 'title') 
        
    def get_users(self, chatRoom):
        return [item.id for item in chatRoom.users.all()]


class ChatRoomAddUserSerializer(ChatRoomBaseSerializer):

    def update(self, instance, validate_data):
        userID = self.context['request'].data.get('userID', -1)
        
        try:
            user = User.objects.get(id=userID)
            instance.users.add(user)
        except ObjectDoesNotExist: 
            pass

        return super().update(instance, validate_data)


class ChatRoomDeleteUserSerializer(ChatRoomBaseSerializer):

    def update(self, instance, validate_data):
        userID = self.context['request'].data.get('userID', -1)
        try:
            instance.users.filter(id=userID).delete()
        except ObjectDoesNotExist: 
            pass

        return super().update(instance, validate_data)


class UserSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all()) #
    chatRooms = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'chatRooms', 'messages',) # ,   
    
    def get_chatRooms(self, user):
        return list(user.chatRooms.values_list('id', flat=True))
        

class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    chatRoom = serializers.ReadOnlyField(source='chatRoom.id')


    class Meta:
        model = Message
        fields = ('id', 'owner', 'chatRoom', 'date', 'message')

