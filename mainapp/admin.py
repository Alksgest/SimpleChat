from django.contrib import admin

from .models import ChatRoom, User, Message


admin.site.register(ChatRoom)
admin.site.register(User)
admin.site.register(Message)

# Register your models here.
