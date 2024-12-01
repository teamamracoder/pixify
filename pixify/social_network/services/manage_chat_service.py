from ..packages.get_data import GetData
from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404
from django.db.models import Q



def manage_list_chats(sort_by='title'):
  return Chat.objects.all().order_by(sort_by)

def manage_create_chats(title,type,created_by,chat_cover):
  return Chat.objects.create(title=title,type=type,created_by=created_by,chat_cover=chat_cover)

def manage_get_member(chat_id): 
    chat_members = ChatMember.objects.filter(chat_id=chat_id )
    member_id = [member.member_id for member in chat_members]
    chat_member = User.objects.filter(id=1)
    return chat_member

#  def get_chat_member_by_member_id(chat_id):
#     chat_members = ChatMember.objects.filter(chat_id=chat_id)
#     user_chat_members = [member.user for member in chat_members]
#     return user_chat_members


def manage_get_chat(chat_id):
   return get_object_or_404 (Chat , id=chat_id)
    

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

def manage_list_chats_filtered(search_query, sorting_order, sort_by, page_number):
    
    # get data
    data = (
        GetData(Chat)
        .search(search_query,"title","type","chat_cover")
        .sort(sort_by, sorting_order)
        .paginate(limit=10, page=page_number)
        .execute()
    )
    # return data
    return data

