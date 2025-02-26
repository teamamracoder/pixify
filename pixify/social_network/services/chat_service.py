from ..constants import ChatType, MessageDeleteType
from ..models import Chat, User, ChatMember, Follower, Message, MessageReadStatus
from django.shortcuts import get_object_or_404
from django.db.models.functions import Coalesce
from django.db.models.functions import Coalesce, Concat
from datetime import date
from django.db.models import (
    CharField, Case, When, Value, F, Q, Max, Exists, Subquery, OuterRef
)
from django.db.models.functions import Coalesce, Concat


def list_chats_by_user(user):
    user_chats = Chat.objects.filter(
        members=user,
        is_active=True,
    ).annotate(
        is_member_active=Exists(
            ChatMember.objects.filter(
                chat_id=OuterRef('id'),
                member_id=user,
                is_active=True
            )
        )
    ).filter(is_member_active=True
    ).annotate(
        latest_message_timestamp=Coalesce(
            Max(
                'fk_chat_messages_chats_id__send_at',
                filter=Q(
                    ~Q(fk_chat_messages_chats_id__delete_type=MessageDeleteType.DELETED_FOR_EVERYONE.value) &
                    ~Q(fk_chat_messages_chats_id__deleted_by__contains=[user.id])
                )
            ),
            F('created_at')
        )
    ).annotate(
        latest_message=Subquery(
            Message.objects.filter(
                Q(chat_id=OuterRef('pk')),
                Q(is_active=True),
                ~Q(delete_type=MessageDeleteType.DELETED_FOR_EVERYONE.value),
                ~Q(deleted_by__contains=[user.id]),
                (
                    (Q(text__isnull=False) & ~Q(text="")) |
                    (Q(media_url__isnull=False) & ~Q(media_url=[])) |
                    Q(post_id__isnull=False)
                )
            ).order_by('-send_at')
            .annotate(
                message_content=Case(
                    When(~Q(text="") & Q(text__isnull=False), then=F('text')),
                    When(~Q(media_url=[]) & Q(media_url__isnull=False), then=Value("📷 Image")),
                    When(
                        Q(post_id__isnull=False),
                        then=Case(
                            # If the sender of the post is the user, show "You sent a reels"
                            When(sender_id=user.id, then=Value("You sent a posts")),
                            # Otherwise, show "Sender's First Name sent a reels"
                            default=Concat(
                                Subquery(
                                    Message.objects.filter(id=OuterRef('id'))
                                    .values('sender_id__first_name')[:1]
                                ),
                                Value(" sent a reels"),
                                output_field=CharField()
                            ),
                            output_field=CharField()
                        )
                    ),
                    default=Value(""),
                    output_field=CharField()
                )
            )
            .values('message_content')[:1]
        )
    ).annotate(
        latest_message_sender_id=Subquery(
            Message.objects.filter(
                Q(chat_id=OuterRef('pk')),
                Q(is_active=True),
                ~Q(delete_type=MessageDeleteType.DELETED_FOR_EVERYONE.value),
                ~Q(deleted_by__contains=[user.id])
            ).order_by('-send_at')
            .values('sender_id')[:1]
        )
    ).order_by('-latest_message_timestamp')

    user_chats = user_chats.filter(
        Q(latest_message__isnull=False) | Q(type=ChatType.GROUP.value)
    )

    chat_data = []
    for chat in user_chats:
        latest_message = Message.objects.filter(
            chat_id=chat.id,
            is_active=True
        ).exclude(
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
        filtered_chats =[]
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






def list_followers_birthday(user):
    try:
        today = date.today()

        # Filter followings who have birthdays today and exclude the user themselves
        followings = Follower.objects.filter(
            follower=user,  # Only the people the user follows
            is_active=True,
            user_id__dob__month=today.month,
            user_id__dob__day=today.day,

        ).exclude(user_id=user).values(  # Exclude the user's own profile
            'user_id',
            'user_id__first_name',
            'user_id__last_name',
            'user_id__profile_photo_url',
            'user_id__dob'
        )
    except Exception:
        followings = []

    return {'followings': list(followings)}

def list_followings(user, offset=0, limit=5):
    try:
        followings = Follower.objects.filter(
            follower=user,
            is_active=True
        ).exclude(user_id=user).values(
            'user_id',
            'user_id__first_name',
            'user_id__last_name',
            'user_id__profile_photo_url'
        )[offset:offset + limit]
    except Exception:
        followings = []

    return {'followings': followings}



def list_top_chats_api(request, user):
    search_query = request.GET.get('search', '')
    chats = Chat.objects.filter(members=user, is_active=True)
    
    # Filter chats if a search query is provided
    if search_query:
        chats = chats.filter(
            Q(members__first_name__icontains=search_query) |
            Q(members__last_name__icontains=search_query)
        )
    
    chat_data_list = []
    
    for chat in chats:
        # Get the message count for each chat
        message_count = Message.objects.filter(chat_id=chat).count()
        
        if chat.type == ChatType.PERSONAL.value:
            member = get_recipient_for_personal(chat.id, user)
            title = f"{member.first_name} {member.last_name}"
            chat_cover = member.profile_photo_url or '/images/avatar.jpg'
        elif chat.type == ChatType.GROUP.value:
            title = chat.title or get_recipients_for_group(chat.id, user)
            chat_cover = chat.chat_cover or '/images/group_pic.png'
        
        # Build a dictionary with all needed info
        chat_info = {
            'id': chat.id,
            'title': title,
            'chat_cover': chat_cover,
            'message_count': message_count,
        }
        chat_data_list.append(chat_info)
    
    # Sort the list by message count in descending order and return only the top 3
    chat_data_list.sort(key=lambda c: c['message_count'], reverse=True)
    return chat_data_list[:6]




def is_message_seen_by_user(message, user):
    seen = MessageReadStatus.objects.filter(message_id=message, read_by=user, is_active=True).exists()
    
    return seen