from django.urls import re_path,path 
from . import consumers

websocket_urlpatterns = [
    path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi()),
    path(r'ws/socket-servers/<int:id>/', consumers.NewConsumer.as_asgi()),
    path(r'ws/<int:myid>/<int:id>/',consumers.PersonalChatConsumer.as_asgi()),


]