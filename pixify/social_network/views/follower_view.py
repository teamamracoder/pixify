from django.shortcuts import render,redirect
from django.views import View
from ..services import chat_service
from django.http import JsonResponse

class FollowerListViewApi(View):
    def get(self, request):
        user = request.user
        follower_data = chat_service.list_followers_api(request, user)
        return JsonResponse(follower_data, safe=False) 
    

