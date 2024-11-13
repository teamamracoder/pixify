from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404

def list_chats():
    return Chat.objects.all()

def chat_details(chat_id):
    return get_object_or_404(Chat, id=chat_id)

def create_chat(title, members, chat_cover, user,type):
            
    chat = Chat.objects.create(title=title, members=members, chat_cover=chat_cover, created_by=user,type=type)        

    for member_id in members:
        member = User.objects.get(id=member_id)
        ChatMember.objects.create(chat_id=chat, member_id=member, created_by=user)
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