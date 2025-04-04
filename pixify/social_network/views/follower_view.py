from django.views import View 
from ..services import follower_service,chat_member_service,user_service
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
            'follow_button_types': follow_button_types,
            'current_user':current_user
        })


class FollowingListView(View):
    def get(self, request, user_id):
        current_user = request.user.id
        followings = follower_service.get_all_following_details(user_id)  # People the user follows
        current_user_followers = follower_service.get_all_follower_details(current_user)  # People who follow the user
        current_user_followings = follower_service.get_all_following_details(current_user)  # People the user follows

        follow_button_types = []

        for following in followings:
            following_id = following.get('id')

            if following_id == current_user:
                continue  # Skip current user

            if following_id in [f.get('id') for f in current_user_followings]:
                button_type = 'unfollow'  # You are already following them
            elif following_id in [f.get('id') for f in current_user_followers]:
                button_type = 'follow-back'  # They follow you, but you don’t follow them
            else:
                button_type = 'follow'  # Neither follows each other

            follow_button_types.append({
                'id': following_id,
                'button_type': button_type
            })

        return render(request, 'enduser/follow/following.html', {
            'followings': followings,
            'follow_button_types': follow_button_types,
            'current_user': current_user
        })



class FollowCreateView(View):
    def post(self, request, user_id):
        current_user = request.user

        follower_id = user_service.get_user_obj(user_id)
        if current_user == follower_id:
            return JsonResponse({'status': 'error', 'message': 'You cannot follow yourself'}, status=400)

        # Check if the follow relationship already exists
        created = follower_service.create_follow(user_id,current_user)

        if created:
            return JsonResponse({'status': 'success', 'message': 'Followed successfully', 'button': 'unfollow'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Already following this user'}, status=400)
        
        
class FollowBackCreateView(View):
    def post(self, request, user_id):
        current_user = request.user
        follower_id = user_service.get_user_obj(user_id)

        if current_user == follower_id:
            return JsonResponse({'status': 'error', 'message': 'You cannot follow-back yourself'}, status=400)

        # Check if the follow relationship already exists
        created = follower_service.create_follow(user_id, current_user)

        if created:
            return JsonResponse({
                'status': 'success',
                'message': 'Follow-back successfully',
                'button': 'unfollow'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Already following this user'
            }, status=400)
        

class UnfollowCreateView(View):
    def post(self, request, user_id):
        current_user = request.user
        follower_id = user_service.get_user_obj(user_id)
        
        if current_user == follower_id:
            return JsonResponse({'status': 'error', 'message': 'You cannot unfollow yourself'}, status=400)

        # Check if the follow relationship exists
        update = follower_service.unfollow(user_id, current_user)
        
        if update:
            # Check if the unfollowed person is following the current user
            is_followed_back = follower_service.is_following_back(current_user, follower_id)
            
            if is_followed_back:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Unfollowed successfully',
                    'button': 'follow-back'
                })
            else:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Unfollowed successfully',
                    'button': 'follow'
                })
        else:
            return JsonResponse({'status': 'error', 'message': 'You are not following this user'}, status=400)






