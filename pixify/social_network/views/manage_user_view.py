from datetime import datetime
import os
from pyexpat.errors import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


from pixify import settings
from social_network.utils.common_utils import print_log
from social_network.constants.default_values import SortingOrder
from social_network.decorators.exception_decorators import catch_error
from social_network.packages.response import success_response

from ..forms.manage_user_forms import ManageAdminProfileUpdateForm, ManageUserUpdateForm
from ..models.user_model import User

from ..decorators.exception_decorators import catch_error
from .. import services
from ..constants import Gender, RelationShipStatus, Role
from django.core.paginator import Paginator   
from django.http import JsonResponse
from ..forms import ManageUserCreateForm

from user_agents import parse




from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.parse import urljoin
import uuid


class ManageUserListView(View):
    @catch_error
    def get(self, request):
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', "created_at")
        sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
        page_number = request.GET.get('page', 1)

        # get data
        data = services.manage_user_service.manage_list_users_filtered(
            search_query=search_query,
            sort_by=sort_by,
            sorting_order=sort_order,
            page_number=page_number
        )

        # add more data
        data["choices_gender"] = [{gender.value: gender.name} for gender in Gender]

        # return
        return render(
            request,
            'adminuser/user/list.html',
            success_response("User data fetched successfully", data)
        ) 

class ManageUserCreateView(View):
    @catch_error
    def get(self, request):
        form = ManageUserCreateForm()
        choices_gender = [{type.value: type.name} for type in Gender]
        choices_relationship = [{type.value: type.name} for type in RelationShipStatus]
        return render(request, 'adminuser/user/create.html', {"form": form,"choices_gender":choices_gender,"choices_relationship":choices_relationship})

    @catch_error
    def post(self, request):
        user = request.user
        form = ManageUserCreateForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            user_data = {
                'first_name': form.cleaned_data['first_name'],
                'middle_name': form.cleaned_data['middle_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'gender': form.cleaned_data['gender'],
                'address': form.cleaned_data['address'],
                'relationship_status': form.cleaned_data['relationship_status'],
                'hobbies': form.cleaned_data['hobbies'],
                'roles': [1],  # Set the default role
                'created_by': user
            }

            # Get the 'dob' field
            dob = form.cleaned_data.get('dob')
            if not dob or dob == '':
                # Set a default dob value if empty
                dob = datetime(2000, 1, 1)  # Default Date: 2000-01-01

            user_data['dob'] = dob

            # Check if dob is invalid (e.g., '0000-00-00')
            if dob.year == 0 and dob.month == 0 and dob.day == 0:
                dob = datetime(2000, 1, 1)  # Set to a valid default date

            # Pass the user data to the service function to create the user
            services.manage_user_service.manage_create_user(**user_data)

            # Redirect to the user list after successful creation
            return redirect('user_list')

        # If form is invalid, render the form with errors
        return render(request, 'adminuser/user/create.html', success_response(
                message=messages),
                {"form": form})

class ManageUserDetailView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        parsed_user_agent = parse(user_agent)

        # Extract browser info
        browser = parsed_user_agent.browser.family
        os = parsed_user_agent.os.family
        device = parsed_user_agent.device.family

        # Add this information to the context
        context = {
            'user': user,
            'browser': browser,
            'os': os,
            'device': device,
        }
        user = services.manage_user_service.manage_get_user(user_id)
        all_post_count = services.manage_user_service.get_all_posts_by_user(user_id)
        all_follower_count = services.manage_user_service.get_all_followers_by_user(user_id)
        activity ={
            'posts':all_post_count,
            'followers':all_follower_count
        }
        return render(request, 'adminuser/user/detail.html', {'user': user, 'context':context,'activity':activity})
    
class ManageUserUpdateView(View):
    @catch_error
    def get(self, request, user_id):
        # choices_gender = [{gender.value: gender.name} for gender in Gender]
        # choices_relationship_status = [{relationship_status.value: relationship_status.name} for relationship_status in RelationShipStatus]
       
        user = get_object_or_404(User, id=user_id)

        # Pre-populate form with existing user data
        form = ManageUserUpdateForm(initial={
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            # 'email': user.email,
            # 'gender': user.gender,
            'address': user.address,
            # 'relationship_status': user.relationship_status,
            'hobbies': user.hobbies,
            'dob': user.dob
        })

        return render(request, 'adminuser/user/update.html', {
            'form': form,
            'user': user,
            # 'choices_gender': choices_gender,
            # 'choices_relationship_status': choices_relationship_status
        })

    @catch_error
    def post(self, request, user_id):
        choices_gender = [{gender.value: gender.name} for gender in Gender]
        choices_relationship_status = [{relationship_status.value: relationship_status.name} for relationship_status in RelationShipStatus]
        login_user = request.user
        user = get_object_or_404(User, id=user_id)

        form = ManageUserUpdateForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.middle_name = form.cleaned_data.get('middle_name', '')  # Default to empty string if None
            user.last_name = form.cleaned_data['last_name']

            # Only update email if it has changed
            # new_email = form.cleaned_data['email']
            # if new_email != user.email:  # If email is different from the current one
            #     user.email = new_email
    
            # user.gender = form.cleaned_data['gender']
            user.address = form.cleaned_data['address']
            user.hobbies = form.cleaned_data['hobbies']
            # user.relationship_status = form.cleaned_data['relationship_status']
            
            dob = form.cleaned_data.get('dob')
            if dob:
                user.dob = dob
            else:
                user.dob = None  # Set default value (None) for blank D.O.B.

            user.updated_by = login_user
            user.save()  # Save the updated user instance

            return redirect('user_list')  # Redirect to the list page after successful save

        # Render form with errors if invalid
        return render(request, 'adminuser/user/update.html', {
            'form': form,
            'user_id': user.id,
            # 'choices_gender': choices_gender,
            # 'choices_relationship_status': choices_relationship_status
        })
    
class ManageToggleUserActiveView(View):
    def post(self, request, user_id):
        user = services.manage_user_service.manage_get_user(user_id)
        user.is_active = not user.is_active  # Toggle active status
        user.save()
        return JsonResponse({'is_active': user.is_active})

# class ManageAdminProfileView(View):
    
    
#     @catch_error
#     def get(self, request, user_id):
#         user = get_object_or_404(User, id=user_id)  # Assuming you have a User model
#         print (user)
#         form = ManageAdminProfileUpdateForm(initial={
#             'first_name': user.first_name,
#             'middle_name': user.middle_name,
#             'last_name': user.last_name,
#             'address': user.address,
#             'hobbies': user.hobbies,
#             'dob': user.dob       
#         })
#         return render(request,  'admin/users/profile/', {"form": form, "user_id": user.id})
#     @catch_error
#     def post(self, request, user_id):
        
#         user = get_object_or_404(User, id=user_id)

#         form = ManageAdminProfileUpdateForm(request.POST)

#         if form.is_valid():
#             user.first_name = form.cleaned_data['first_name']
#             user.middle_name = form.cleaned_data.get('middle_name', '')  # Default to empty string if None
#             user.last_name = form.cleaned_data['last_name']
#             user.address = form.cleaned_data['address']
#             user.hobbies = form.cleaned_data['hobbies']
#             dob = form.cleaned_data.get('dob')
#             if dob:
#                 user.dob = dob
#             else:
#                 user.dob = None  # Set default value (None) for blank D.O.B.

#             user.updated_by = user
#             user.save()  # Save the updated user instance

#             return redirect(' admin/users/profile/')  # Redirect to the list page after successful save

#         # Render form with errors if invalid
#         return render(request, ' admin/users/profile/', {
#             'form': form,
#             'user_id': user.id,
#         })
class ManageAdminProfileView(View):
    
    @catch_error
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)  
        form = ManageAdminProfileUpdateForm(initial={
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'address': user.address,
            'hobbies': ", ".join(user.hobbies) if user.hobbies else "",
            'dob': user.dob       
        })
        return render(request, 'adminuser/user/user_profile.html', {"form": form, "user_id": user.id})

    @catch_error
    def post(self, request, user_id):
        login_user=request.user
        user = get_object_or_404(User, id=user_id)
        form = ManageAdminProfileUpdateForm(request.POST)
        print(user)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.middle_name = form.cleaned_data.get('middle_name', '')
            user.last_name = form.cleaned_data['last_name']
            user.address = form.cleaned_data['address']
            user.hobbies = form.cleaned_data['hobbies']
            # user.dob = form.cleaned_data.get('dob', None)  
            dob = form.cleaned_data.get('dob')
            if dob:
                user.dob = dob
            else:
                user.dob = None 

            user.updated_by = login_user
            user.save()  

            return redirect('user_profile', user_id=user.id)

        return render(request, 'adminuser/user/user_profile.html', {'form': form})

    
    
class ChangeMyThemeView(View):
    def post(self, request):
        theme = request.POST.get('theme')
        user = services.user_service.get_user(request.user.id)
        services.user_service.change_theme(user, ui_mode=theme)
        return JsonResponse(success_response('Theme changed to {theme} mode', {'theme': theme}))






class ManageAdminProfilePicView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        profile_picture = request.FILES.get('profile_picture')
        if not profile_picture:
            return JsonResponse({'success': False, 'message': 'No file uploaded'})

        try:
            # Generate a unique filename
            file_extension = profile_picture.name.split('.')[-1]
            unique_filename = f"profile_pics/{user.id}_{uuid.uuid4().hex}.{file_extension}"
            
            # Save file to media storage
            file_path = default_storage.save(unique_filename, ContentFile(profile_picture.read()))

            # Construct the full URL to access the saved file
            profile_url = urljoin(settings.MEDIA_URL, file_path)

            # Save the URL to the database
            user.profile_photo_url = profile_url
            user.save()

            return JsonResponse({'success': True, 'profile_photo_url': profile_url})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error saving file: {str(e)}'})
        


