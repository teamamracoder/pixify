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

def chat_details(chat_id):
    return get_object_or_404(Chat, id=chat_id)

def create_chat(user, members, type, is_active):
            
    chat = Chat.objects.create(members=members, created_by=user,type=type, is_active=is_active)        

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
def user_follow(user):
    followers = Follower.objects.filter(follower=user, is_active=True).select_related('following')
    followings = Follower.objects.filter(following=user, is_active=True).select_related('follower')
    return followers, followings

def list_chats_api(request,user):
    search_query = request.GET.get('search',)
    if search_query:
        chats = Chat.objects.filter(members=user,title__icontains=search_query).values()
    else:
        chats =  Chat.objects.filter(members=user).values()
    return chats
    
def list_followers_api(request,user):
    search_query = request.GET.get('search','')
    if search_query:
        followers = Follower.objects.filter(follower=user,fk_follower_users__icontains=search_query).values()
        followings = Follower.objects.filter(following=user,fk_following_users__icontains=search_query).values()
    else:
       followers = User.objects.all().values()
    return followers,followings
def chat_member(chat_id,user):
    chat_member = ChatMember.objects.exclude(member_id=user.id).get(chat_id=chat_id)
    member = chat_member.member_id 
    return member


# chat service
# all chats jar title that starts with search param 
# +
# all recepeints jar firstname starts with search param

# considtion
# chats er member er mdhdhe loggeduser thakte lgbe