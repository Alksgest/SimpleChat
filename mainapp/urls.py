from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from mainapp import views

urlpatterns = [
    path('api/', views.api_root),
    path('api/chatRooms', views.ChatRoomList.as_view(), name='chatroom-list'),
    path('api/chatRooms/<int:pk>', views.ChatRoomDetails.as_view(), name='chatroom-detail'),
    path('api/chatRoomAction/<int:pk>', views.ChatRoomAction.as_view(), name='chatroom-action'),
    path('api/chatRooms/chat_room_redirect/', views.ChatRoomRedirect.as_view()),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>', views.UserDetails.as_view(), name='user-detail'),
    path('api/messages', views.MessageList.as_view(), name='message-list'),
    path('api/messages/<int:pk>',views.MessageDetails.as_view(), name='message-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
