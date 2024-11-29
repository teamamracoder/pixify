from ..models import Follower
from django.db.models import Q

def list_followers_api(request, user):
    search_query = request.GET.get('search', '')
    if search_query:
        followers = Follower.objects.filter(follower=user).filter(
            Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query)
        ).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')

        followings = Follower.objects.filter(following=user).filter(
            Q(user_id__first_name__icontains=search_query) | Q(user_id__last_name__icontains=search_query)
        ).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')
        
    else:
        followers = Follower.objects.filter(follower=user).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')
        followings = Follower.objects.filter(following=user).values('user_id', 'user_id__first_name', 'user_id__last_name', 'user_id__email', 'user_id__profile_photo_url')

    response_data = {'followers': list(followers), 'followings': list(followings)}
    return response_data