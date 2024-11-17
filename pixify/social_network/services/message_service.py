from ..models import Message, MessageReadStatus,MessageMention
from django.shortcuts import get_object_or_404


def list_messages_by_chat_id(chat_id):   # make message_read_status service and views for read_status
    return Message.objects.filter(chat_id=chat_id,is_active=True)

def create_message(text, media_url, sender_id, chat_id):
    return Message.objects.create(
        text=text,
        media_url=media_url,
        sender_id_id=sender_id,
        chat_id_id=chat_id
    )

def get_message_by_id(message_id):
    return get_object_or_404(Message, id=message_id,is_active=True)

def update_message(message, text, media_url):
    message.text = text
    message.media_url = media_url
    message.save()
    return message

def delete_message(message_id):
        message = get_object_or_404(message, id=message_id)
        message.is_active=False
        message.save()

def reply_message(user, text, media_url, sender_id, chat_id, reply_for_message_id):    
    message = Message.objects.create(
        text=text,
        media_url=media_url,
        sender_id=sender_id,
        chat_id=chat_id,
        reply_for_message_id=reply_for_message_id,
    )
        
    return message    

def unread_count(chat,user):    
    unread_count = Message.objects.filter(
        chat_id=chat
        ).exclude(
        fk_message_msg_status_messages_id__read_by=user
    ).count()  
    return unread_count
