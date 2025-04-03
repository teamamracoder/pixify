from datetime import datetime
from pyexpat.errors import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from social_network.utils.common_utils import print_log
from social_network.constants.default_values import SortingOrder
from social_network.decorators.exception_decorators import catch_error
from social_network.packages.response import success_response

from ..forms.manage_user_forms import ManageUserUpdateForm
from ..models.user_model import User

from ..decorators.exception_decorators import catch_error

from .. import services
from ..constants import Gender, RelationShipStatus, Role
from django.core.paginator import Paginator
from django.http import JsonResponse
from ..forms import ManageUserCreateForm


class ManageUserUpdateView(View):
    @catch_error
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)  # Assuming you have a User model
        form = ManageUserUpdateForm(initial={
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'email': user.email
        })
        return render(request, 'adminuser/user/update.html', {"form": form, "user_id": user.id})

#     @catch_error
#     def post(self, request, user_id):
#         choices_gender = [{gender.value: gender.name} for gender in Gender]
#         choices_relationship_status = [{relationship_status.value: relationship_status.name} for relationship_status in RelationShipStatus]
#         login_user = request.user
#         user = get_object_or_404(User, id=user_id)

#         form = ManageUserUpdateForm(request.POST)

#         if form.is_valid():
#             user.first_name = form.cleaned_data['first_name']
#             user.middle_name = form.cleaned_data.get('middle_name', '')  # Default to empty string if None
#             user.last_name = form.cleaned_data['last_name']

#             # Only update email if it has changed
#             new_email = form.cleaned_data['email']
#             if new_email != user.email:  # If email is different from the current one
#                 user.email = new_email
    
#             user.gender = form.cleaned_data['gender']
#             user.address = form.cleaned_data['address']
#             user.hobbies = form.cleaned_data['hobbies']
#             user.relationship_status = form.cleaned_data['relationship_status']
            
#             dob = form.cleaned_data.get('dob')
#             if dob:
#                 user.dob = dob
#             else:
#                 user.dob = None  # Set default value (None) for blank D.O.B.

#             user.updated_by = login_user
#             user.save()  # Save the updated user instance

#             return redirect('user_list')  # Redirect to the list page after successful save

#         # Render form with errors if invalid
#         return render(request, 'adminuser/user/update.html', {
#             'form': form,
#             'user_id': user.id,
#             'choices_gender': choices_gender,
#             'choices_relationship_status': choices_relationship_status
#         })

# class ManageUserDeleteView(View):
#     def get(self, request, user_id):
#         user = services.manage_user_service.manage_get_user(user_id)
#         return render(request, 'adminuser/user/delete.html', {'user': user})

    def post(self, request, user_id):
        user = services.manage_user_service.manage_get_user(user_id)
        services.user_service.delete_user(user)
        return redirect('user_list')

class ManageToggleUserActiveView(View):
    def post(self, request, user_id):
        user = services.manage_user_service.manage_get_user(user_id)
        user.is_active = not user.is_active  # Toggle active status
        user.save()
        return JsonResponse({'is_active': user.is_active})

class ManageUserProfileView(View):
    def get(self, request):
        return render(request, 'adminuser/user/user_profile.html')

class ChangeMyThemeView(View):
    def post(self, request):
        theme = request.POST.get('theme')
        user = services.user_service.get_user(request.user.id)
        services.user_service.change_theme(user, ui_mode=theme)
        return JsonResponse(success_response('Theme changed to {theme} mode', {'theme': theme}))
    

class UserSearchApi(View):
    def get(self, request):
        data = services.user_service.user_search_api(request)
        return JsonResponse(data)

        
