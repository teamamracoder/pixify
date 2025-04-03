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
    def get(self,request,user_id):
        followers=follower_service.get_all_follower_details(user_id)
        print(followers)
        return render(request,'enduser/follow/follower.html',{'followers':followers})
    
class FollowingListView(View):
    def get(self,request,user_id):
        followings = follower_service.get_all_following_details(user_id)
        return render(request,'enduser/follow/following.html',{'followings':followings})
    

