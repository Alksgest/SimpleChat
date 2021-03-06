from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from .models import ChatRoom, Message, User
from .constants import MAX_USER_COUNT

from datetime import datetime



class ChatRoomBaseSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('users', )

    def get_users(self, chatRoom):
        return [item.id for item in chatRoom.users.all()]


class ChatRoomSerializer(ChatRoomBaseSerializer):
    messages = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Message.objects.all())

    class Meta:
        model = ChatRoom
        fields = ('id', 'messages', 'users', 'title')


class ChatRoomAddUserSerializer(ChatRoomBaseSerializer):

    def update(self, instance, validate_data):
        userID = self.context['request'].data.get('userID', -1)

        try:
            user = User.objects.get(id=userID)
            if user not in instance.users.all() and instance.users.all().count() < MAX_USER_COUNT: #mb add 2 custom Exception classes
                instance.users.add(user)
                # instance.users.save()
            else:
                raise Exception

        except ObjectDoesNotExist:
            pass
        except Exception:
            pass

        return super().update(instance, validate_data)


class ChatRoomPostMessageSerializer(ChatRoomBaseSerializer):

    def update(self, instance, validate_data):
        #userID = self.context['request'].data.get('userID', -1)
        #user = User.objects.get(id=userID)
        raw_message = self.context['request'].data.get('message', -1)

        message = Message()
        message.message = raw_message.get('message', '')
        message.date = datetime.strptime(raw_message.get('date'), '%Y-%m-%d %H:%M') #TODO add tzinfo
        message.owner = User.objects.get(id=raw_message.get('owner'))
        message.chatRoom = ChatRoom.objects.get(id=raw_message.get('chatRoom'))

        message.save()

        instance.messages.add(message)

        return super().update(instance, validate_data)


class ChatRoomDeleteUserSerializer(ChatRoomBaseSerializer):

    def update(self, instance, validate_data):
        userID = self.context['request'].data.get('userID', -1)
        try:
            user = User.objects.get(id=userID)
            if user in instance.usesrs.all():
                instance.users.remove(user)
        except ObjectDoesNotExist:
            pass

        return super().update(instance, validate_data)


class UserSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Message.objects.all())
    chatRooms = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'chatRooms', 'messages',)  # ,

    def get_chatRooms(self, user):
        return list(user.chatRooms.values_list('id', flat=True))


class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    chatRoom = serializers.ReadOnlyField(source='chatRoom.id')

    class Meta:
        model = Message
        fields = ('id', 'owner', 'chatRoom', 'date', 'message')
