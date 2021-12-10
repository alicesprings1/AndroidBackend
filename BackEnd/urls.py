from django.urls import path
from .views import *

urlpatterns = [
    path('get_chatrooms', GetChatRooms.as_view()),
    path('get_messages',GetMessages.as_view()),
    path('send_message',PubMessage.as_view()),
    path('submit_push_token',PubToken.as_view())
]
