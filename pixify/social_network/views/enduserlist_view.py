import os
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.views import View

from pixify import settings
from ..services import user_service
from ..constants import Gender
from ..constants import RelationShipStatus
from ..services import chat_service
from django.http import JsonResponse
from ..services import manage_notification_service
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import Notification

class EnduserprofileListView(View):
    def get(self,request,user_id):
        user = user_id
        data = chat_service.list_followings(user_id, 0, 5)
        user_details = [user_service.get_user_details(user_id)]
        friends = user_service.friends_count(user_id)
        user_data = []

        for detail in user_details:
            dob = detail.dob
            age = user_service.calculate_age(dob)
            user_data.append({
                'first_name': detail.first_name,
                'last_name': detail.last_name,
                'profile_photo': detail.profile_photo_url,
                'age': age,
                'status': detail.is_active,
                'friends': friends,
            })
        return render(request,'enduser/profile/index.html',{'followings': data['followings'], 'user_data': user_data})