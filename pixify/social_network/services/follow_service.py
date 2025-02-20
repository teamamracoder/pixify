from ..models import User,Follower
from django.db.models import Q

def getAllRecommendedusers(user_id,followed_users):
    return User.objects.exclude(Q(id=user_id) | Q(id__in=followed_users)).values('id', 'first_name', 'middle_name','last_name','profile_photo_url')

def getFollowed_users(user_id):
    return Follower.objects.filter(user_id=user_id).values_list('following', flat=True)

def getLastFollowername(user_id,followed_users):
    last_follower = Follower.objects.filter(following=user_id, user_id__in=followed_users).order_by('-created_at').values('user_id').first()
    if last_follower:
        return User.objects.filter(id=last_follower['user_id']).values('first_name').first()
    else:
        return None
        #print("Last follower:", last_follower_name)
    #return User.objects.filter(id=last_follower['user_id']).values('first_name').first()

def getTotal_followers(user_id,followed_users):
    return Follower.objects.filter(following=user_id,user_id__in=followed_users).count()

def CreateFollowing(following_id,user_id):
    instance_user_id=User.objects.get(id=user_id)
    instance_following_id=User.objects.get(id=following_id)
    Follower.objects.create(user_id=instance_user_id,following=instance_following_id,created_by=instance_user_id)