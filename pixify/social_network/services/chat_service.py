from ..models import Chat, User, ChatMember,Follower,Message
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Max
# badhan
from datetime import date

from django.db.models import Max,Q,Subquery,OuterRef,F
from django.db.models.functions import Coalesce
from social_network.utils.common_utils import print_log

def list_chats_by_user(user):
    user_chats = Chat.objects.filter(
        members=user,
        is_active=True
        ).annotate(
        # Use Coalesce to fallback to created_at if no messages exist
        latest_message_timestamp=Coalesce(
            Max('fk_chat_messages_chats_id__send_at', filter=Q(is_active=True)),
            F('created_at')
        )
    ).order_by('-latest_message_timestamp')

    user_chats = user_chats.annotate(
        latest_message=Subquery(
            Message.objects.filter(
                chat_id=OuterRef('pk'),
                is_active=True
            ).order_by('-created_at')
            .values('text')[:1]
        )
    )
    return user_chats


def create_chat(user,title,chat_cover,type):
    chat = Chat.objects.create(title=title,chat_cover=chat_cover,type=type,created_by=user)
    return chat

def update_chat(chat, title, chat_cover,user):
    chat.title = title
    chat.chat_cover = chat_cover
    chat.updated_by=user
    chat.save()
    return chat

def delete_chat(chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.is_active = False
    chat.save()
    return chat

def get_chat_by_id(chat_id):
    return get_object_or_404(Chat, id=chat_id, is_active=True)

def get_recipient_for_personal(chat_id,user):
    # check this
    try:
        chat_member = ChatMember.objects.exclude(member_id=user.id).get(chat_id=chat_id)
        if chat_member:
            member = chat_member.member_id
            return member
        return False
    except Exception as e:
        return False

def count_members(chat_id ):
    members=ChatMember.objects.filter(chat_id=chat_id)
    return members



def get_recipients_for_group(chat_id,user):
        chat_members = ChatMember.objects.filter(chat_id=chat_id)
        first_names = [
        'You' if chat_member.member_id == user else chat_member.member_id.first_name
        for chat_member in chat_members
    ]
        return " , ".join(first_names)

def get_all_user_follow(user):
    followers = Follower.objects.filter(follower=user, is_active=True).select_related('following')
    followings = Follower.objects.filter(following=user, is_active=True).select_related('follower')
    return followers, followings

def list_chats_api(request,chat_data_list):
    search_query =request.GET.get('search', '')
    if search_query:
        chats = Chat.objects.filter(members=user, title__icontains=search_query).values()
    else:
        chats = Chat.objects.filter(members=user).values()
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


