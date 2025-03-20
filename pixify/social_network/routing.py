from django.urls import re_path
from . import consumers
from .callconsumer import CallConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/call/(?P<chat_id>\w+)/$',CallConsumer.as_asgi()),    
]
