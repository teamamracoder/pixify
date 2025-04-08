from datetime import datetime  # Import datetime module for handling dates
from pyexpat.errors import messages  # Import messages for error handling
from django.http import HttpResponseBadRequest, JsonResponse  # Import HTTP response classes
from django.shortcuts import get_object_or_404, render, redirect  # Import shortcuts for common Django operations
from django.views import View  # Import View class for class-based views
from social_network.utils.common_utils import print_log  # Import logging utility
from social_network.constants.default_values import SortingOrder  # Import sorting order constants
from social_network.decorators.exception_decorators import catch_error  # Import decorator for error handling
from social_network.packages.response import success_response  # Import success response helper
from ..forms.manage_user_forms import ManageAdminProfileUpdateForm, ManageUserUpdateForm  # Import user management forms
from ..models.user_model import User  # Import User model
from ..import services  # Import services module
from ..constants import Gender, RelationShipStatus, Role  # Import user-related constants
from django.core.paginator import Paginator  # Import Paginator for pagination
from user_agents import parse  # Import user agent parser to extract device/browser details
from django.core.files.storage import default_storage  # Import storage utility for handling file uploads
from django.core.files.base import ContentFile  # Import ContentFile to create file-like objects
from django.conf import settings  # Import settings for accessing Django configurations
import uuid  # Import UUID module for generating unique identifiers
from urllib.parse import urljoin  # Import urljoin for constructing URLs
from ..forms import ManageUserCreateForm # import the user form

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
        # Fetch user data by ID
        user = User.objects.get(id=user_id)
        
        # Get the user agent string from the request
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Parse the user agent to extract browser, OS, and device info
        parsed_user_agent = parse(user_agent)
        
        # Extract browser name
        browser = parsed_user_agent.browser.family
        
        # Extract operating system name
        os = parsed_user_agent.os.family
        
        # Extract device type
        device = parsed_user_agent.device.family

        # Prepare context dictionary to pass to the template
        context = {
            'user': user,
            'browser': browser,
            'os': os,
            'device': device,
        }
        
        # Fetch user details using service function
        user = services.manage_user_service.manage_get_user(user_id)
        
        # Fetch count of all posts by the user
        all_post_count = services.manage_user_service.get_all_posts_by_user(user_id)
        
        # Fetch count of all followers of the user
        all_follower_count = services.manage_user_service.get_all_followers_by_user(user_id)
        
        # Prepare activity dictionary
        activity ={
            'posts': all_post_count,
            'followers': all_follower_count
        }
        
        # Render user detail page with user data, context, and activity details
        return render(request, 'adminuser/user/detail.html', {'user': user, 'context': context, 'activity': activity})


class ManageUserUpdateView(View):
    @catch_error
    def get(self, request, user_id):
        # Fetch the user object by ID
        user = get_object_or_404(User, id=user_id)

        # Pre-populate form with existing user data
        form = ManageUserUpdateForm(initial={
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'address': user.address,
            'hobbies': user.hobbies,
            'dob': user.dob
        })

        # Render the update user page with the pre-filled form
        return render(request, 'adminuser/user/update.html', {
            'form': form,
            'user': user
        })

    @catch_error
    def post(self, request, user_id):
        # Fetch the user object by ID
        user = get_object_or_404(User, id=user_id)
        form = ManageUserUpdateForm(request.POST)

        if form.is_valid():
            # Prepare user data for update
            user_data = {
                'first_name': form.cleaned_data['first_name'],
                'middle_name': form.cleaned_data.get('middle_name', ''),  # Default to empty if None
                'last_name': form.cleaned_data['last_name'],
                'address': form.cleaned_data['address'],
                'hobbies': form.cleaned_data['hobbies'],
                'dob': form.cleaned_data.get('dob', None),  # Default None if empty
                'updated_by': request.user
            }

            # Call the service function to update the user
            services.manage_user_service.manage_update_user(user_id, **user_data)

            # Redirect to the user list page after successful update
            return redirect('user_list')

        # Render form with errors if invalid
        return render(request, 'adminuser/user/update.html', {
            'form': form,
            'user_id': user.id
        })


class ManageToggleUserActiveView(View):
    def post(self, request, user_id):
        # Fetch user data by ID
        user = services.manage_user_service.manage_get_user(user_id)
        # Toggle active status
        user.is_active = not user.is_active
        user.save()
        # Return the updated status as JSON response
        return JsonResponse({'is_active': user.is_active})


class ManageUserProfileView(View):
    def get(self, request):
        return render(request, 'adminuser/user/user_profile.html')


class ChangeMyThemeView(View):
    def post(self, request):
        # Get the theme preference from the POST request
        theme = request.POST.get('theme')
        # Retrieve the logged-in user details
        user = services.user_service.get_user(request.user.id)
        # Update the user's theme preference
        services.user_service.change_theme(user, ui_mode=theme)
        # Return a success response with the updated theme mode
        return JsonResponse(success_response('Theme changed to {theme} mode', {'theme': theme}))


class ManageAdminProfileUpdateView(View):
    @catch_error
    def get(self, request, user_id):
        # Retrieve the user object by ID, or return a 404 error if not found
        user = get_object_or_404(User, id=user_id)
        # Initialize the form with the existing user details
        form = ManageAdminProfileUpdateForm(initial={
            'first_name': user.first_name,
            'middle_name': user.middle_name,
            'last_name': user.last_name,
            'address': user.address,
            'hobbies': ", ".join(user.hobbies) if user.hobbies else "",
            'dob': user.dob
        })
        # Render the user profile update template with the form
        return render(request, 'adminuser/user/user_profile.html', {"form": form, "user_id": user.id})

    @catch_error
    def post(self, request, user_id):
        # Get the currently logged-in user
        login_user = request.user
         # Initialize the form with POST data
        form = ManageAdminProfileUpdateForm(request.POST)

        if form.is_valid():
            # Prepare user data for updating
            user_data = {
                'first_name': form.cleaned_data['first_name'],
                'middle_name': form.cleaned_data.get('middle_name', ''),
                'last_name': form.cleaned_data['last_name'],
                'address': form.cleaned_data['address'],
                'hobbies': form.cleaned_data['hobbies'],
                'dob': form.cleaned_data.get('dob', None),
                'updated_by': login_user
            }

            # Call the service function to update the user profile
            services.manage_user_service.manage_update_admin_profile(user_id, **user_data)

            # Redirect to the user profile update page after a successful update
            return redirect('user_profile_update', user_id=user_id)

        # Render the user profile update page again with the form containing validation errors
        return render(request, 'adminuser/user/user_profile.html', {'form': form})


class ManageAdminProfilePicView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        profile_picture = request.FILES.get('profile_picture')
        if not profile_picture:
            return JsonResponse({'success': False, 'message': 'No file uploaded'})

        try:
            # Generate a unique filename and save the file
            file_extension = profile_picture.name.split('.')[-1]
            unique_filename = f"profile_pics/{user.id}_{uuid.uuid4().hex}.{file_extension}"

            # Save file and get the file path
            file_path = default_storage.save(unique_filename, ContentFile(profile_picture.read()))

            # Construct the profile URL
            profile_url = urljoin(settings.MEDIA_URL, file_path)

            # Update user's profile photo URL and save
            user.profile_photo_url = profile_url
            user.save()

            return JsonResponse({'success': True, 'profile_photo_url': profile_url})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error saving file: {str(e)}'})

