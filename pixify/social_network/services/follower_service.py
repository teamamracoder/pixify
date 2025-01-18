from ..models import Follower
from django.db.models import Q

def list_followers_api(request, user):
    search_query = request.GET.get('search', '')
    if search_query:
        followers = Follower.objects.filter(following=user).filter(
            Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query)
        ).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')

        followings = Follower.objects.filter(follower=user).filter(
            Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query)
        ).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')
        
    else:
        followers = Follower.objects.filter(following=user).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')
        followings = Follower.objects.filter(follower=user).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')

    combined_list = list(followers) + list(followings)    
    unique_members = {member['user_id']: member for member in combined_list}.values()

    response_data = {
        'members': list(unique_members),
    }
    return response_data


def members_list_api(request, user, chat_members):
    search_query = request.GET.get('search', '')

    followers_query = Follower.objects.filter(following=user)
    followings_query = Follower.objects.filter(follower=user)

    if search_query:
        followers_query = followers_query.filter(Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query))
        followings_query = followings_query.filter(Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query))

    followers_query = followers_query.exclude(user_id__in=chat_members)
    followings_query = followings_query.exclude(user_id__in=chat_members)

    follower_fields = ['user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url']
    following_fields = ['user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url']
    
    followers = followers_query.values(*follower_fields)
    followings = followings_query.values(*following_fields)
    
    combined_list = list(followers) + list(followings)    
    unique_members = {member['user_id']: member for member in combined_list}.values()

    response_data = {
        'members': list(unique_members),
    }
    return response_data

