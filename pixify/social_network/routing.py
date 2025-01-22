from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', consumers.ChatConsumer.as_asgi()),  # Capture chat_id dynamically
    re_path(r'ws/call/(?P<call_id>[a-zA-Z0-9]+)/$', consumers.CallConsumer.as_asgi()),
]
