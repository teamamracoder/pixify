import os
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.views import View

from pixify import settings
from ..services import user_service
from ..constants import Gender
from ..constants import RelationShipStatus
from ..services import chat_service,message_service
from django.http import JsonResponse
from ..services import manage_notification_service
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import Notification

class EnduserprofileView(View):
    def get(self, request):
        user = request.user

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', 5))
            data = chat_service.list_followings(user, offset, limit)
            return JsonResponse({'followings': list(data['followings'])}, safe=False)

        else:
            user = request.user
            data = chat_service.list_followings(user, 0, 5)
            user_details = [user_service.get_user_details(user.id)]
            friends = user_service.friends_count(user.id)
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

            return render(
                request,
                'enduser/profile/index.html',
                {'followings': data['followings'], 'user_data': user_data}
            )


# class EnduserprofileUpdateView(View):
#     def get(self, request, user_id):
#         user_details = user_service.get_user_details(user_id)
#         print(user_details)
#         return render(request, 'enduser/profile/editprofile.html',
#         'enduser/profile/index.html', {'user_details': user_details})

#     def post(self, request, user_id):
#         user_details = user_service.get_user_details(user_id)

#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         gender = request.POST.get('gender')
#         address = request.POST.get('address')
#         dob = request.POST.get('dob')
#         country = request.POST.get('country')
#         bio= request.POST.get('bio')
#         if request.method == 'POST':
#          hobbies = request.POST.get('hobbies', '')
#          hobbies_list = [hobby.strip() for hobby in hobbies.split(',')] if hobbies else []
#          hobbies = hobbies_list
#         gender_mapping = {'Male': Gender.MALE.value, 'Female': Gender.FEMALE.value, 'Other': Gender.OTHER.value}
#         gender = gender_mapping.get(gender, None)
#         relationship_status = request.POST.get('relationship_status')
#         relationship_status_mapping = {
#             'Single': RelationShipStatus.SINGLE.value,
#             'Married': RelationShipStatus.MARRIED.value,
#             'Divorced': RelationShipStatus.DIVORCED.value,
#             'Widowed': RelationShipStatus.WIDOWED.value,
#             'Other': RelationShipStatus.OTHER.value,
#         }
#         relationship_status = relationship_status_mapping.get(relationship_status, None)
#         profile_picture = request.FILES.get('profile_picture')


#         user_service.update_user(user_id, first_name, last_name, email, phone, gender,address,dob,country,bio,hobbies,relationship_status, profile_picture)

#         return render(request, 'enduser/profile/index.html', {'user_details': user_details, 'errors': "An error occurred"})

class EnduserprofileUpdateView(View):
    def get(self, request, user_id):
        user_details = user_service.get_user_details(user_id)
        #print(user_details)
        return render(request, 'enduser/profile/editprofile.html', {'user_details': user_details})

    def post(self, request, user_id):
        user_details = user_service.get_user_details(user_id)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        dob = request.POST.get('dob') or None
        country = request.POST.get('country')
        bio = request.POST.get('bio')
        if request.method == 'POST':
            hobbies = request.POST.get('hobbies', '')
            hobbies_list = [hobby.strip() for hobby in hobbies.split(',')] if hobbies else []
            hobbies = hobbies_list
        gender_mapping = {'Male': Gender.MALE.value, 'Female': Gender.FEMALE.value, 'Other': Gender.OTHER.value}
        gender = gender_mapping.get(gender, None)
        relationship_status = request.POST.get('relationship_status')
        relationship_status_mapping = {
            'Single': RelationShipStatus.SINGLE.value,
            'Married': RelationShipStatus.MARRIED.value,
            'Divorced': RelationShipStatus.DIVORCED.value,
            'Widowed': RelationShipStatus.WIDOWED.value,
            'Other': RelationShipStatus.OTHER.value,
        }
        relationship_status = relationship_status_mapping.get(relationship_status, None)
        profile_file = request.FILES.get('profile_picture')
        if profile_file:
            profile_file_path = os.path.join(settings.MEDIA_ROOT, profile_file.name)
            with open(profile_file_path, 'wb+') as destination:
              for chunk in profile_file.chunks():
                 destination.write(chunk)
            profile_picture=(f"{settings.MEDIA_URL}{profile_file.name}")
        else :
           profile_picture = None

        user_service.update_user(user_id, first_name, last_name, email, phone, gender, address, dob, country, bio, hobbies, relationship_status, profile_picture)

        #return render(request, 'enduser/profile/index.html', {'user_details': user_details, 'errors': "An error occurred"})
        return redirect('userprofile')


# def edit_information(request):
#     if request.method == "POST":
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success')
#     else:
#         form = UserProfileForm()
#     return render(request, 'edit_information.html', {'form': form})


@login_required
def unread_notifications_count(request):
    user = request.user
    unread_count = Notification.objects.filter(receiver_id=user, is_read=False).count()
    if unread_count > 10:
        unread_count = '10+'
    elif unread_count== 0:
        unread_count = ''
    return JsonResponse({'unread_count': unread_count})




@login_required
def unread_messages_count(request): 
    user=request.user        #unread message show
    unread_msg_count=message_service.unread_msg_count(user.id)
    if unread_msg_count > 10:
        unread_msg_count = '10+'
    elif unread_msg_count== 0:
        unread_msg_count = ''
    return JsonResponse({'unread_msg_count': unread_msg_count})
    

        