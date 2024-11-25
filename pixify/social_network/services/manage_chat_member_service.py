from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404
from django.db.models import Q




def manage_member_create_chats(member_id,chat_id):
  return ChatMember.objects.create(member_id=member_id,chat_id=chat_id)

def manage_member_list_chats_filtered(search_query, sort_by='title'):
    if search_query:
        
        return ChatMember.objects.filter(
            Q(title__icontains=search_query) | 
            Q(type__icontains=search_query) |
            Q(chat_cover__icontains=search_query)
        ).order_by(sort_by)
    return ChatMember.objects.all().order_by(sort_by)
