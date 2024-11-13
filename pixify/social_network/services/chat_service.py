from .. import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def list_chats(user):
    return models.Chat.objects.filter(members=user).exclude(members=user)

def chats_create(request):
    title = request.data.get('title')
    chat_type = request.data.get('type')
    members = request.data.get('members')
    chat_cover = request.data.get('chat_cover')
    is_active = request.data.get('is_active', True)
    created_by = request.user.id  
    updated_by = request.user.id  
    chat = chats_create(title, chat_type, members, chat_cover, is_active, created_by, updated_by)
    return models.Chat.objects.create(title=title,type=type,members=members,chat_cover=chat_cover,is_active=is_active ,created_by=created_by,updated_by=updated_by)

# chat_service.py

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


    

def delete_chat(chat_id):
    return get_object_or_404(models.Chat, id=chat_id)

def details_chats():
    return models.Chat.objects.all()

def get_chat (chat_id):
    return get_object_or_404(models.Chat, id=chat_id)