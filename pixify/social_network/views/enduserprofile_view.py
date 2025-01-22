from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.views import View
from ..services import user_service
from ..constants import Gender
from ..constants import RelationShipStatus
from ..services import chat_service
from django.http import JsonResponse
from ..services import manage_notification_service 

class EnduserprofileView(View):
    def get(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request to load more profiles
            user = request.user
            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', 5))
            data = chat_service.list_followings(user, offset, limit)
            return JsonResponse({'followings': list(data['followings'])}, safe=False)
        else:
            # Initial page load
            user = request.user
            data = chat_service.list_followings(user, 0, 5)  
            user_details=user_service.get_user_details(user.id)# Load first 5 profiles
            friends=user_service.friends_count(user.id)
            user_data = []
            for detail in user_details:
                dob=detail.dob
                age=user_service.calculate_age(dob)
                user_data.append({
                    'first_name': detail.first_name,
                    'last_name': detail.last_name,
                    'profile_photo':detail.profile_photo_url,
                    'age':age,
                    'status':detail.is_active,
                    'friends':friends,
                })
            return render(
                request,
                'enduser/profile/index.html',
                {'followings': data['followings'], 'user_data': user_data}
            )
        
from django.shortcuts import render
from ..services import manage_notification_service 

def unread_notifications(request):
    """
    Display a page with a list of unread notifications for the logged-in user.
    """
    user_id = request.user.id  # Assuming the user is authenticated
    unread_notifications = manage_notification_service.manage_list_notifications_filtered().filter(
        receiver_id=user_id, is_read=False, is_active=True
    )
    unread_count = manage_notification_service.unread_notifications_count(user_id)
    
    print(f"Unread count: {unread_count}")  # Debug statement to check unread count
    
    return render(request, 'enduser/profile/editprofile.html', {
        'unread_notifications': unread_notifications,
        'unread_count': unread_count,
    })


# from django.shortcuts import render
# from django.views import View
# from ..services import user_service

# class UserProfileUpdateView(View):
#     def get(self, request):
#         # Fetch user profile data from the service
#         user = request.user
#         profile_data = user_service.get_user_profile(user)

#         # Pass the data to the template
#         return render(request, 'enduser/profile/index.html', {'profile': profile_data})  working 20/01/2025

    
  
# class UserprofileView(View): no need
#     def get(self, request):
#         return render(request, 'enduser/profile/userprofile.html')  

# Work By Badhan
class EnduserprofileUpdateView(View):
    def get(self, request, user_id):
        user_details = user_service.get_user_details(user_id)
        print(user_details)
        return render(request, 'enduser/profile/editprofile.html', {'user_details': user_details})

    def post(self, request, user_id):
        user_details = user_service.get_user_details(user_id)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        address = request.POST.get('address') 
        dob = request.POST.get('dob')
        country = request.POST.get('country') 
        bio= request.POST.get('bio')
        if request.method == 'POST':
         hobbies = request.POST.get('hobbies', '')
         hobbies_list = [hobby.strip() for hobby in hobbies.split(',')] if hobbies else []        
         hobbies = hobbies_list
        # Convert gender value to integer
        gender_mapping = {'Male': Gender.MALE.value, 'Female': Gender.FEMALE.value, 'Other': Gender.OTHER.value}
        gender = gender_mapping.get(gender, None)
        # convert relationship into integer
        relationship_status = request.POST.get('relationship_status')
        relationship_status_mapping = {
            'Single': RelationShipStatus.SINGLE.value,         
            'Married': RelationShipStatus.MARRIED.value,         
            'Divorced': RelationShipStatus.DIVORCED.value,         
            'Widowed': RelationShipStatus.WIDOWED.value,         
            'Other': RelationShipStatus.OTHER.value,         
        }
        relationship_status = relationship_status_mapping.get(relationship_status, None)
        profile_picture = request.FILES.get('profile_picture') 
 

        user_service.update_user(user_id, first_name, last_name, email, phone, gender,address,dob,country,bio,hobbies,relationship_status, profile_picture)

        return render(request, 'enduser/profile/index.html', {'user_details': user_details, 'errors': "An error occurred"}) 


# End by Badhan


def edit_information(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('success')  
    else:
        form = UserProfileForm()
    return render(request, 'edit_information.html', {'form': form})






