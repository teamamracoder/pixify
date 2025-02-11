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
        chat_member = ChatMember.objects.exclude(member_id=user.id).get(chat_id=chat_id,is_active=True)
        if chat_member:
            member = chat_member.member_id
            return member
        return False
    except Exception as e:
        return False

def members(chat_id ):
    members=ChatMember.objects.filter(chat_id=chat_id,is_active=True)
    return members

def chat_members(chat_id):
    members = ChatMember.objects.filter(chat_id=chat_id, is_active=True)
    return list(members.values("member_id"))  # Return user IDs instead



def get_recipients_for_group(chat_id,user):
        chat_members = ChatMember.objects.filter(chat_id=chat_id,is_active=True)
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
        chat_title = chat.title
    chat_data = {
        'id': chat.id,
        'title': chat_title,
        'chat_cover': chat.chat_cover if chat.chat_cover else '/static/images/group_pic.png',
        'created_by':chat.created_by,
        'is_group': chat.type == ChatType.GROUP.value,
        'members': [
            {
                'id': member.member_id,
                'first_name': "You" if member.member_id.id == user else member.member_id.first_name +" "+ member.member_id.last_name,
                'profile': member.member_id.profile_photo_url if member.member_id.profile_photo_url else '/static/images/avatar.jpg'
            }
            for member in active_members
        ]
    }

    return chat_data
def latest_message_sender_name(chat_latest_message_sender_id, user_id):
    if user_id == chat_latest_message_sender_id:
        sender_name = 'You'
    else:
        # Fetch the sender's first name from the User model
        sender = User.objects.filter(id=chat_latest_message_sender_id).values('first_name').first()
        sender_name = sender['first_name'] if sender else ''  # Safely access first_name

    # Return the name as a dictionary
    name = {
        'sender_name': sender_name
    }
    return name


def message_seen_status(message):
    members_count = ChatMember.objects.filter(
        chat_id=message.chat_id,
        is_active=True
    ).count()

    read_by_count = MessageReadStatus.objects.filter(
        message_id=message,
        is_active=True
    ).values('read_by').distinct().count()

    if read_by_count == members_count:
        read_status = True
    else:
        read_status = False

    return read_status





