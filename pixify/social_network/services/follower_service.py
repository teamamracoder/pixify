from datetime import date
from ..models import Follower, Chat, ChatMember
from django.db.models import Q, OuterRef, Subquery
from ..constants import ChatType


def list_followers_api(request, user):
    search_query = request.GET.get('search', '')
    if search_query:
        followers = Follower.objects.filter(following=user, is_active=True).filter(
            Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query)
        ).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')

        followings = Follower.objects.filter(user_id=user, is_active=True).filter(
            Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query)
        ).values('following', 'following__first_name', 'following__last_name', 'following__email', 'following__profile_photo_url')

    else:
        followers = Follower.objects.filter(following=user, is_active=True).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')
        followings = Follower.objects.filter(user_id=user, is_active=True).values('following', 'following__first_name', 'following__last_name', 'following__email', 'following__profile_photo_url')

    combined_list = followers.union(followings)

    response_data = {
        'members': list(combined_list),
    }
    return response_data


def members_list_api(request, user, chat_members):
    search_query = request.GET.get('search', '')

    followers_query = Follower.objects.filter(following=user, is_active=True)
    followings_query = Follower.objects.filter(user_id=user, is_active=True)

    if search_query:
        followers_query = followers_query.filter(Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query))
        followings_query = followings_query.filter(Q(following__first_name__icontains=search_query) | Q(following__last_name__icontains=search_query))

    followers_query = followers_query.exclude(user_id__in=chat_members)
    followings_query = followings_query.exclude(following__in=chat_members)

    follower_fields = ['user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url']
    following_fields = ['following', 'following__first_name', 'following__last_name', 'following__email', 'following__profile_photo_url']

    followers = followers_query.values(*follower_fields)
    followings = followings_query.values(*following_fields)

    combined_list = followers.union(followings)

    response_data = {
        'members': list(combined_list),
    }
    return response_data

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



def list_follow_api(request, user):
    search_query = request.GET.get('search', '')

    other_member_subquery = ChatMember.objects.filter(
        chat_id=OuterRef('pk'),
        is_active=True
    ).exclude(member_id=user.id).values('member_id')[:1]

    # Filter personal chats and annotate them with the other member's ID.
    chats = Chat.objects.filter(
        members=user,
        is_active=True,
        type=ChatType.PERSONAL.value
    ).annotate(
        other_member=Subquery(other_member_subquery)
    )

    # Now you can easily retrieve a list of other member IDs:
    mem1 = list(chats.values_list('other_member', flat=True))

    if search_query:
        followers = Follower.objects.filter(following=user, is_active=True).filter(
            Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query)
        ).exclude(user_id__in=mem1).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url', 'user_id__bio')

        followings = Follower.objects.filter(user_id=user, is_active=True).filter(
            Q(following__first_name__icontains=search_query) | Q(following__last_name__icontains=search_query)
        ).exclude(following__in=mem1).values('following', 'following__first_name', 'following__last_name', 'following__email', 'following__profile_photo_url', 'following__bio')

    else:

        followers = Follower.objects.filter(following=user, is_active=True).exclude(user_id__in=mem1).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url', 'user_id__bio')
        followings = Follower.objects.filter(user_id=user, is_active=True).exclude(following__in=mem1).values('following', 'following__first_name', 'following__last_name', 'following__email', 'following__profile_photo_url', 'following__bio')
  
    combined_list = followers.union(followings)
    
    
    response_data = {
        'members': list(combined_list),
    }

    return response_data


def follower_check(posted_by,user):
    return Follower.objects.filter(user_id=user,following=posted_by).exists()


def get_all_following_details(user):
    following_list = Follower.objects.filter(user_id=user, is_active=True).exclude(following=user).select_related('following')
    followings_data = [
        {
            "id": f.following.id,  # Extracting correct user ID
            "fullname": f"{f.following.first_name} {f.following.last_name}",
            "profile_pic": f.following.profile_photo_url
        }
        for f in following_list
    ]
    return followings_data


def get_all_follower_details(user):
    follower_list = Follower.objects.filter(following=user, is_active=True).exclude(created_by=user).select_related('created_by')
    follower_data = [
        {
            "id": f.following.id,  # Extracting correct user ID
            "fullname": f"{f.following.first_name} {f.following.last_name}",
            "profile_pic": f.following.profile_photo_url
        }
        for f in follower_list
    ]
    return follower_data
    
