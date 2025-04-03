from django.views import View 
from ..services import follower_service,chat_member_service
from django.http import JsonResponse 
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from django.shortcuts import render

 
class FollowerListViewApi(View): 
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request): 
        user = request.user 
        follower_data = follower_service.list_followers_api(request, user)
        return JsonResponse(follower_data, safe=False)
    
class MemberListViewApi(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self,request,chat_id):
        user = request.user 
        chat_id = chat_id
        chat_member = chat_member_service.get_chat_members(chat_id)
        
        member_data = follower_service.members_list_api(request, user,chat_member) 

        return JsonResponse(member_data, safe=False)

    
class FollowerListView(View):
    def get(self, request, user_id):
        current_user = request.user.id
        followers = follower_service.get_all_follower_details(user_id)
        current_user_followers = follower_service.get_all_follower_details(current_user)
        current_user_followings = follower_service.get_all_following_details(current_user)

        # Create a list to store button types for each follower along with their id
        follow_button_types = []

        for follower in followers:
            follower_id = follower.get('id')  # Get the follower's ID from the dictionary

            if follower_id == current_user:
                continue

            # Determine the button type for this follower
            if follower_id in [following.get('id') for following in current_user_followings]:
                button_type = 'unfollow'
            elif follower_id in [follower.get('id') for follower in current_user_followers]:
                button_type = 'follow-back'
            else:
                button_type = 'follow'

            # Append the button type along with follower id
            follow_button_types.append({
                'id': follower_id,
                'button_type': button_type
            })

        return render(request, 'enduser/follow/follower.html', {
            'followers': followers,
            'current_user_followers': current_user_followers,
            'current_user_followings': current_user_followings,
            'follow_button_types': follow_button_types
        })


class FollowingListView(View):
    def get(self, request, user_id):
        current_user = request.user.id
        followings = follower_service.get_all_following_details(user_id)
        current_user_followers = follower_service.get_all_follower_details(current_user)
        current_user_followings = follower_service.get_all_following_details(current_user)

        # Create a list to store button types for each following along with their id
        follow_button_types = []

        for following in followings:
            following_id = following.get('id')  # Get the following's ID from the dictionary

            # If the following is the current user, skip adding button for them
            if following_id == current_user:
                continue

            # Determine the button type for this following
            if following_id in [follower.get('id') for follower in current_user_followers]:
                button_type = 'follow-back'
            elif following_id in [follower.get('id') for follower in current_user_followings]:
                button_type = 'unfollow'
            else:
                button_type = 'follow'

            # Append the button type along with following id
            follow_button_types.append({
                'id': following_id,
                'button_type': button_type
            })

        return render(request, 'enduser/follow/following.html', {
            'followings': followings,
            'current_user_followers': current_user_followers,
            'current_user_followings': current_user_followings,
            'follow_button_types': follow_button_types
        })






