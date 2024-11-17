from ..models import Chat, User, ChatMember,Follower
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Max


def list_chats(user):
    user_chats = Chat.objects.filter(members=user).annotate(
        latest_message_timestamp=Max('fk_chat_messages_chats_id__send_at'),
        latest_message=Max('fk_chat_messages_chats_id__text')  
    ).order_by('-latest_message_timestamp')
    return user_chats

def create_chat(titel,chat_cover,type):
    chat = Chat.objects.create(titel=titel,chat_cover=chat_cover,type=type)  
    return chat

def update_chat(chat, title, chat_cover):    
    chat.title = title  
    chat.chat_cover = chat_cover                               
    chat.save()
    return chat    

def delete_chat(chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.is_active = False
    chat.save()
    return chat
  
def get_chat(chat_id):
    return get_object_or_404(Chat, id=chat_id)
  
def chat_member(chat_id,user):
    chat_member = ChatMember.objects.exclude(member_id=user.id).get(chat_id=chat_id)
    member = chat_member.member_id 
    return member

def user_follow(user):
    followers = Follower.objects.filter(follower=user, is_active=True).select_related('following')
    followings = Follower.objects.filter(following=user, is_active=True).select_related('follower')
    return followers, followings
  
def mention_chat(chat,user):     
     return ChatMember.objects.fillter(chat_id=chat).exclude(member_id=user).selct_related('member')

def list_chats_api(request, user):
    search_query = request.GET.get('search', '')
    if search_query:
        chats = Chat.objects.filter(members=user, title__icontains=search_query).values()
    else:
        chats = Chat.objects.filter(members=user).values()
    print(chats)
    return chats
  
def list_followers_api(request, user):
    search_query = request.GET.get('search', '')
    if search_query:        
        followers = Follower.objects.filter(
            follower=user, user_id__first_name__icontains=search_query
        ).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email','user_id__profile_photo_url')
        followings = Follower.objects.filter(
            following=user, user_id__first_name__icontains=search_query
        ).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email','user_id__profile_photo_url')
    else:
        followers = []
        followings =[]

    response_data = { 'followers': list(followers), 'followings': list(followings) }
    return response_data

