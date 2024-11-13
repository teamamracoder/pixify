from .. import models
from django.shortcuts import get_object_or_404

def list_chats():
  return models.Chat.objects.all()


def create_chats(title,type,is_active,created_at,updated_at,created_by_id,updated_by_id,chat_cover):
  return models.Chat.objects.create(title=title,type=type,is_active=is_active,created_at=created_at,updated_at=updated_at,created_by_id=created_by_id,updated_by_id=updated_by_id,chat_cover=chat_cover)

def get_chat(chat_id):
    return get_object_or_404(models.Chat, id=chat_id)

def update_chats(chat,title,type,is_active,created_at,updated_at,created_by_id,updated_by_id,chat_cover):
   chat.title=title
   chat.type=type
   chat.is_active=is_active
   chat.created_at=created_at
   chat.updated_at=updated_at
   chat.created_by_id=created_by_id
   chat.updated_by_id=updated_by_id
   chat.chat_cover=chat_cover
   
   chat.save()
   return chat

def delete_chats(chat):
    chat.delete()