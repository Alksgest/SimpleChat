from rest_framework import serializers

from .models import ChatRoom, Message, User

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all())
    #messages_ids = serializers.SerializerMethodField()
    #users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = ChatRoom
        fields = ('id', 'messages', 'users', 'title') #'messages_ids' 
        
    # def get_messages_ids(self, chatRoom):
    #     queryset = Message.objects.filter(chatRoom_id=chatRoom.id)
    #     return queryset
    

    # def get_users(self, chatRoom):
    #     # queryset = User.objects.filter(chatRooms__id=chatRoom.id)
    #     queryset = User.objects.all()
    #     return queryset


class UserSerializer(serializers.ModelSerializer):
    #messages = serializers.SerializerMethodField()
    messages = serializers.PrimaryKeyRelatedField(many=True, queryset=Message.objects.all()) #
    #chatRooms = serializers.ManyRelatedField(source='chatRooms', child_relation=)
    chatRooms = serializers.SerializerMethodField()
   #chatRooms = ChatRoomSerializer(read_only=True, many=True, )
    #chatRooms = serializers.ReadOnlyField(source='chatRooms.id')

    class Meta:
        model = User
        fields = ('id', 'username', 'chatRooms', 'messages',) # ,   
    
    def get_chatRooms(self, user):
        #queryset = ChatRoom.objects.filter(id__in=user.chatRooms.id)
        queryset = ChatRoom.objects.filter(id__in=user.chatRooms.values_list('id'))
        #queryset = ChatRoom.objects.filter(id__in=[item.id for item in user.chatRooms.objects.all()])
        #queryset = ChatRoom.objects.all()
        return queryset
        

    # def get_messages(self, user):
    #     queryset = Message.objects.filter(owner__id=user.id)
    #     return queryset


class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    chatRoom = serializers.ReadOnlyField(source='chatRoom.id')
    # owner = UserSerializer(read_only=True)
    # chatRoom = ChatRoomSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ('id', 'owner', 'chatRoom', 'date', 'message') # 'owner', 'chatRoom'

