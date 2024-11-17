from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404
from django.db.models import Q


# def list_chats():
#   return models.Chat.objects.all()
def list_chats(sort_by='title'):
    return Chat.objects.all().order_by(sort_by)


def create_chats(**kwargs):
  chat= Chat.objects.create(
     title=kwargs['title'],
     type=kwargs['type'],
     chat_cover=kwargs.get('chat_cover'),
     is_active=kwargs.get('is_active', True),
     created_by=kwargs['created_by']

  )
  return chat

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



