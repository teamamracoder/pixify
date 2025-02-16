# from django.shortcuts import render
# from django.views import View
# from ..services import chat_service

# class BirthdayView(View):
#     def get(self, request):
#         user = request.user
#         data = chat_service.list_followers_birthday(user)

#         # Helper function to extract (month, day) for sorting
#         def get_month_day(dob):
#             if dob is None:
#                 return (13, 0)  # Place None dates at the end
#             return (dob.month, dob.day)

#         # Combine followers and followings into one list
#         combined_list = data['followings']


#         # Sort the combined list by month and day
#         combined_list = sorted(combined_list, key=lambda x: get_month_day(x.get('user_id__dob')))

#         # Pass the combined list to the template
#         return render(request, 'enduser/birthday/index.html', {'users': combined_list})
# # data['followers']

#-------------------------------------------use---------------------------------
from django.shortcuts import render
from django.views import View
from datetime import date
from ..services import chat_service,follower_service

class BirthdayView(View):
    def get(self, request):
        user = request.user
        data = follower_service.list_followers_birthday(user)

        # Today's date
        today = date.today()

        # Filter followings with a birthday today and exclude the logged-in user
        combined_list = [
            follower for follower in data['followings']
            if follower['user_id__dob'] and
               follower['user_id__dob'].month == today.month and  #working
               follower['user_id__dob'].day == today.day and
               follower['user_id'] != user.id


            # following for following in data['followings']
            # if following['following_id__dob'] and
            #    following['following_id__dob'].month ==today.month and          need this
            #    following['following_id__dob'].day ==today.day and
            #    following['following_id'] != user.id
        ]

        # Sort the list by (month, day) just in case of further filtering
        combined_list = sorted(combined_list, key=lambda x: (x['user_id__dob'].month, x['user_id__dob'].day))
        # combined_list = sorted(combined_list, key=lambda x: (x['following_id__dob'].month, x['following_id__dob'].day))
        # Pass the filtered and sorted list to the template
        return render(request, 'enduser/birthday/index.html', {'users': combined_list})


