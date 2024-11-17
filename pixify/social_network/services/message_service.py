from ..models import Message,MessageReadStatus
from django.shortcuts import get_object_or_404

def list_messages_by_chat_id(chat_id, unread_messages,user):
            for message in unread_messages:
                MessageReadStatus.objects.create(
                message_id=message,
                read_by=user
            )
            return Message.objects.filter(chat_id=chat_id,is_active=True)


def create_message(text, media_url, sender_id, chat_id):
    return Message.objects.create(
        text=text,
        media_url=media_url,
        sender_id_id=sender_id,
        chat_id_id=chat_id
    )

def get_message(message_id):
    return get_object_or_404(Message, id=message_id)

def update_message(message, text, media_url):
    message.text = text
    message.media_url = media_url
    message.save()
    return message

def delete_message(message_id):
        message = get_object_or_404(message, id=message_id)
        message.is_active=False
        message.save()

def unread_count(chat,user):    
    unread_count = Message.objects.filter(
        chat_id=chat
        ).exclude(
        fk_message_msg_status_messages_id__read_by=user
    ).count()  
    return unread_count