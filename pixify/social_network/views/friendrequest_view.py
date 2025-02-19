from sqlite3 import IntegrityError
import traceback
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from social_network.constants.default_values import Role
from social_network.decorators.auth_decorators import auth_required, role_required
from social_network import services
from django.core.exceptions import ObjectDoesNotExist
from social_network.decorators.exception_decorators import catch_error

class FriendRequestView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        return render(request, 'enduser/friendrequest/index.html')
#To get all Recommended User List
class AllRecommendedUsersView(View):
    def get(self, request):
        user_id=request.user.id
        followed_users=services.follow_service.getFollowed_users(user_id)
        all_users=services.follow_service.getAllRecommendedusers(user_id,followed_users)
        RecommendedUsers = []
        for user in all_users:
            total_followers=services.follow_service.getTotal_followers(user['id'],followed_users)

            if total_followers > 1:
                latest_follower=services.follow_service.getLastFollowername(user['id'],followed_users)
                follow_text = f"Followed by {latest_follower['first_name']} and {total_followers - 1} other"
            elif total_followers == 1:
                latest_follower=services.follow_service.getLastFollowername(user['id'],followed_users)
                follow_text = f"Followed by {latest_follower['first_name']}"
            else:
                follow_text = "No mutual followers yet"

            RecommendedUsers.append({
                'id': user['id'],
                'first_name': user['first_name'],
                'middle_name': user['middle_name'],
                'last_name': user['last_name'],
                'profile_photo_url': user['profile_photo_url'],
                'followers_text': follow_text
            })
        return JsonResponse(RecommendedUsers, safe=False)
#After Clicking Follow Button For Follow
class FollowUserView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request):
        following_id = request.POST.get('following_id')
        user_id = request.user.id

        if not following_id:
            return JsonResponse({"error": "User ID not provided"}, status=400)

        try:
            services.follow_service.CreateFollowing(following_id,user_id)
            return JsonResponse({"message": "Followed successfully"})
        except ObjectDoesNotExist:  # User doesn't exist
            return JsonResponse({"error": "User not found"}, status=404)

        except IntegrityError:
            return JsonResponse({"error": "You are already following this user"}, status=400)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=500)