from ..constants import ChatType,MessageDeleteType
from ..models import Chat, User, ChatMember,Follower,Message,MessageReadStatus
from django.shortcuts import get_object_or_404
from django.db.models import Max,Q,Subquery,OuterRef,F
from django.db.models.functions import Coalesce
from social_network.utils.common_utils import print_log


def list_chats_by_user(user):
    user_chats = Chat.objects.filter(
        members=user,
        is_active=True,
    ).annotate(
        latest_message_timestamp=Coalesce(
            Max(
                'fk_chat_messages_chats_id__send_at',
                filter=Q(
                    # Exclude messages that are deleted for everyone or deleted by the user
                    ~Q(fk_chat_messages_chats_id__delete_type=MessageDeleteType.DELETED_FOR_EVERYONE.value) &
                    ~Q(fk_chat_messages_chats_id__deleted_by__contains=[user.id])
                )
            ),
            F('created_at')
        )
    ).annotate(
        latest_message=Subquery(
            Message.objects.filter(
                Q(chat_id=OuterRef('pk')),  # Keyword argument
                Q(is_active=True),          # Keyword argument
            # Exclude deleted messages
                ~Q(delete_type=MessageDeleteType.DELETED_FOR_EVERYONE.value),  # Keyword argument
                ~Q(deleted_by__contains=[user.id])  # Keyword argument
            ).order_by('-send_at')
            .values('text')[:1]
        )
    ).annotate(
        latest_message_sender_id=Subquery(
            Message.objects.filter(
                Q(chat_id=OuterRef('pk')),
                Q(is_active=True),
                # Exclude deleted messages
                ~Q(delete_type=MessageDeleteType.DELETED_FOR_EVERYONE.value) &
                ~Q(deleted_by__contains=[user.id])
            ).order_by('-send_at')
            .values('sender_id')[:1]
        )
    ).order_by('-latest_message_timestamp')

    # Filter out chats with no visible messages or only deleted ones
    user_chats = user_chats.filter(
        Q(latest_message__isnull=False) | Q(type=ChatType.GROUP.value)
    )

    chat_data = []
    for chat in user_chats:
        # Retrieve the last message, ensuring it is not deleted by the user or marked as deleted
        latest_message = Message.objects.filter(chat_id=chat.id, is_active=True).exclude(
            delete_type=MessageDeleteType.DELETED_FOR_EVERYONE.value,
            deleted_by__contains=[user.id]
        ).last()

        seen_by_all = False
        if latest_message:
            seen_by_all = is_message_seen_by_all(latest_message)

        chat_data.append({
            'chat': chat,
            'seen_by_all': seen_by_all,
        })
    
    return chat_data

def is_message_seen_by_all(message):
    members = User.objects.filter(
        chatmember__chat_id=message.chat_id,
        chatmember__is_active=True
    )
    read_by_count = MessageReadStatus.objects.filter(
        message_id=message,
        is_active=True  
    ).values('read_by').distinct().count()
    return read_by_count == members.count()



def create_chat(user,title,chat_cover,type):
    chat = Chat.objects.create(title=title,chat_cover=chat_cover,type=type,created_by=user)
    return chat

def update_chat_title(chat, title, user):
    chat.title = title
    chat.updated_by = user
    chat.save()

def update_chat_bio(chat, bio, user):
    chat.chat_bio = bio
    chat.updated_by = user
    chat.save()

def update_chat_cover(chat, cover_url, user):
    chat.chat_cover = cover_url
    chat.updated_by = user
    chat.save()


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
        filtered_chats = [
            chat for chat in chat_data_list 
            if search_query.lower() in chat['title'].lower()
        ]
    else:
        filtered_chats =''
    return filtered_chats

def get_existing_personal_chat(type, user_id, member):
    chats = Chat.objects.filter(type=type)

    for chat in chats:
        members = list(chat.members.values_list('id', flat=True))
        if len(members) == 2 and user_id in members and member in members:
            return chat
    return None

def list_chats_by_user_api(user):
    user_chats = Chat.objects.filter(
        members=user,
        is_active=True
    )
    return user_chats

def chat_details(chat_id, user):
    chat = get_object_or_404(Chat, id=chat_id)
    active_members = ChatMember.objects.filter(chat_id=chat, is_active=True)
    if not chat.title and active_members.exists():
        chat_title = ', '.join([member.member_id.first_name if member.member_id.id != user else "You" for member in active_members])
    else:
        chat_title = chat.title
    chat_data = {
        'id': chat.id,
        'title': chat_title,
        'chat_cover': chat.chat_cover if chat.chat_cover else '/static/images/group_pic.png', 
        'created_by':chat.created_by,
        'is_group': chat.type == ChatType.GROUP.value,
        'chat_bio':chat.chat_bio,
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




