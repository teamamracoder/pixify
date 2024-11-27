from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404
from django.db.models import Q




def manage_member_create_chats(member_id_id,chat_id_id):
  return ChatMember.objects.create(member_id_id=member_id_id,chat_id_id=chat_id_id)

def manage_member_list_chats_filtered(search_query, sort_by='member_id_id'):
    if search_query:
        
        return ChatMember.objects.filter(
            Q(title__icontains=search_query) | 
            Q(type__icontains=search_query) |
            Q(chat_cover__icontains=search_query)
        ).order_by(sort_by)
    return ChatMember.objects.all().order_by(sort_by)
