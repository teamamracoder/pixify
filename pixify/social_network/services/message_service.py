from ..models import Message
from django.shortcuts import get_object_or_404


def list_messages_by_chat_id(chat_id):
    return Message.objects.filter(chat_id=chat_id)
def get_message(message_id):
    return get_object_or_404(Message, id=message_id)
