from ..models import Message,MessageReadStatus,MasterList
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ..constants import MasterType



def list_messages_by_chat_id(chat_id,user_id):  
    messages = Message.objects.filter(chat_id=chat_id, is_active=True)
    for message in messages:
        if not MessageReadStatus.objects.filter(message_id=message, read_by_id=user_id).exists():
            MessageReadStatus.objects.create(
                message_id=message,
                read_by_id=user_id,
                read_at=timezone.now(),
                created_by_id=user_id) 
    return messages

def create_message(text, media_url,sender_id, chat):
    return Message.objects.create(
        text=text,
        media_url=media_url,
        sender_id=sender_id,
        chat_id=chat,
        created_by=sender_id
    )

def get_message_by_id(message_id):
    return get_object_or_404(Message, id=message_id,is_active=True)

def update_message(message, text, media_url,user):
    message.text = text
    message.media_url = media_url
    message.updated_by=user
    message.save()
    return message

def delete_message(message,user):
        message.is_active=False
        message.updated_by=user
        message.save()

def reply_message(user, text, media_urls, sender_id, chat_id, reply_for_message):
    return Message.objects.create(
        text=text,
        media_url=media_urls,
        sender_id=sender_id,
        chat_id=chat_id,
        reply_for_message_id=reply_for_message,
        created_by=user
    )
 
def unread_count(chat,user):    
    unread_count = Message.objects.filter(
        chat_id=chat,
        is_active=True
        ).exclude(
        fk_message_msg_status_messages_id__read_by=user
    ).count()  
    return unread_count

def show_reactions():
    reactions = MasterList.objects.filter(type=MasterType.REACTION.value, is_active=True).values("name", "value")
    return list(reactions) 
