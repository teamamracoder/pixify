from ..models import Message

def list_messages_by_chat_id(chat_id):
    return Message.objects.filter(chat_id=chat_id)