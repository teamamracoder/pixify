from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404

def list_chats():
    return Chat.objects.all()

def chat_details(chat_id):
    return get_object_or_404(Chat, id=chat_id)

def create_chat(user, members, type, is_active):
            
    chat = Chat.objects.create(members=members, created_by=user,type=type, is_active=is_active)        

    # for member_id in members:
    #     member = User.objects.get(id=member_id)
    #     ChatMember.objects.create(chat_id=chat, member_id=member, created_by=user)
    return chat

def update_chat(chat, title, members, chat_cover):    
        chat.title = title  
        chat.chat_cover = chat_cover                
        chat.members.clear()                
        for member_id in members:
            member = User.objects.get(id=member_id)
            ChatMember.objects.create(chat_id=chat, member_id=member)                
        chat.save()
        return chat    

def delete_chat(chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.is_active = False
    chat.save()
    return chat


def get_user_data(user_id):    
    followers = User.objects.filter(followers__followed_user=user_id).exclude(id=user_id)
    followings = User.objects.filter(followings__user=user_id).exclude(id=user_id)
    photo = User.profile_photo_url(User, 'profile') 
    
    return {
        'user':user_id,
        'followers': followers,
        'followings': followings,
        'photo': photo,
    }

def details_chats(chat_id):
    return Chat.objects(chat_id)

def get_chat (chat_id):
    return get_object_or_404(Chat, id=chat_id)



#=====================================================
def admin_list_chats():
  return Chat.objects.all()


def admin_create_chats(title,type,is_active,created_at,updated_at,created_by_id,updated_by_id,chat_cover):
  return Chat.objects.create(title=title,type=type,is_active=is_active,created_at=created_at,updated_at=updated_at,created_by_id=created_by_id,updated_by_id=updated_by_id,chat_cover=chat_cover)

def admin_get_chat(chat_id):
    return get_object_or_404(Chat, id=chat_id)

def admin_update_chats(chat,title,type,is_active,created_at,updated_at,created_by_id,updated_by_id,chat_cover):
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

def admin_delete_chats(chat):
    chat.delete()