from django.shortcuts import render
from django.views import View
from datetime import date
from ..services import chat_service,follower_service

class BirthdayView(View):
    def get(self, request):
        user = request.user
        data = follower_service.list_followers_birthday(user)
        today = date.today()
        combined_list = [
            follower for follower in data['followings']
            if follower['user_id__dob'] and
               follower['user_id__dob'].month == today.month and 
               follower['user_id__dob'].day == today.day and
               follower['user_id'] != user.id
        ]
        combined_list = sorted(combined_list, key=lambda x: (x['user_id__dob'].month, x['user_id__dob'].day))
        return render(request, 'enduser/birthday/index.html', {'users': combined_list})


