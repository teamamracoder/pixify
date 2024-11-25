from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404
from django.db.models import Q



def manage_list_chats():
  return Chat.objects.all()

def manage_create_chats(title,type,created_by,chat_cover):
  return Chat.objects.create(title=title,type=type,created_by=created_by,chat_cover=chat_cover)

def manage_get_chat(chat_id):
    return get_object_or_404(Chat, id=chat_id)

def manage_update_chats(chat,title,type,chat_cover, updated_by):
   chat.title=title
   chat.type=type
     
#    chat.created_by=created_by
   chat.chat_cover=chat_cover
   chat.updated_by=updated_by
   
   chat.save()
   return chat

def manage_delete_chats(chat):
    chat.delete()

def manage_list_chats_filtered(search_query, sort_by='title'):
    if search_query:
        
        return Chat.objects.filter(
            Q(title__icontains=search_query) | 
            Q(type__icontains=search_query) |
            Q(chat_cover__icontains=search_query)
        ).order_by(sort_by)
    return Chat.objects.all().order_by(sort_by)


