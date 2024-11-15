from .. import models
from django.shortcuts import get_object_or_404

def list_chats():
  return models.Chat.objects.all()


def create_chats(**kwargs):
  chat= models.Chat.objects.create(
     title=kwargs['title'],
     type=kwargs['type'],
     chat_cover=kwargs.get('chat_cover'),
     created_by=kwargs['created_by'],
     updated_by=kwargs['updated_by'],
     is_active=kwargs.get('is_active', True) 
  )
  return chat

def get_chat(chat_id):
    return get_object_or_404(models.Chat, id=chat_id)

def update_chats(chat,title,type,is_active,chat_cover,created_by, updated_by):
   chat.title=title
   chat.type=type
   chat.is_active=is_active
   chat.created_by=created_by
   chat.chat_cover=chat_cover
   chat.updated_by=updated_by
   
   chat.save()
   return chat

def delete_chats(chat):
    chat.delete()