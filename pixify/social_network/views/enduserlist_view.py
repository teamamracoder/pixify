from django.shortcuts import render
from django.views import View

from ..models import User
from ..services import user_service,chat_service

class EnduserprofileListView(View):
    def get(self, request, user_id):
        detail = user_service.get_user_details(user_id)
        if not detail:
            return render(request, 'enduser/profile/userprofile.html', {'user_details': None})
        follower_list,following_list=chat_service.get_all_user_follow(user_id)
        print(follower_list)
        print(following_list)
        dob = detail.dob
        age = user_service.calculate_age(dob)

        user_details = {
            'user_name': f"{detail.first_name} {detail.last_name}",
            'profile_photo': detail.profile_photo_url if detail.profile_photo_url else '/static/images/avatar.jpg',
            'age': age,
            'status': "Active" if detail.is_active else "Inactive",
            'following_count': len(following_list),  # Ensure these fields exist in your model
            'followers_count': len(follower_list),  # Ensure these fields exist in your model
            'followers': follower_list,
            'followings': following_list,
        }

        return render(request, 'enduser/profile/userprofile.html', {'user_details': user_details})
