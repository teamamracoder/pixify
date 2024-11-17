from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from .. import services
from ..constants import Gender, RelationShipStatus, Role
from django.core.paginator import Paginator   
from django.http import JsonResponse



class AdminUserListView(View):
    def get(self, request):
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '') 
        sort_by = request.GET.get('sort_by', 'first_name')
        sort_order = request.GET.get('sort_order', 'asc')
        page_number = request.GET.get('page', 1)

        # Adjust sort order for descending order
        if sort_order == 'desc':
            sort_by = '-' + sort_by

        print(f"Search Query: {search_query}")
        # Get filtered and sorted users based on search
        users = services.user_service.admin_list_users_filtered(search_query, sort_by)

        # Paginate the users
        paginator = Paginator(users, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)

        choices_gender = [{gender.value: gender.name} for gender in Gender]

        return render(request, 'adminuser/user/list.html', {
            'users': page_obj,
            'choices_gender': choices_gender,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })



class AdminUserCreateView(View):
    def get(self, request):
        choices_gender = [{gender.value: gender.name} for gender in Gender]
        choices_relationship_status = [{status.name: status.value} for status in RelationShipStatus]
        return render(request, 'adminuser/user/create.html',{"choices_gender":choices_gender,"choices_relationship_status":choices_relationship_status})

    def post(self, request):
        user_data = {
                    'first_name' : request.POST['first_name'],
                    'middle_name' : request.POST['middle_name'],
                    'last_name' : request.POST['last_name'],
                    'email' : request.POST['email'],
                    'address' : request.POST['address'],
                    'dob' : request.POST['dob'],
                    'gender' : request.POST['gender'],
                    'relationship_status' : request.POST['relationship_status'],
                    'hobbies' : request.POST.getlist('hobbies'),
                    'roles': [1]
                }
        services.user_service.admin_create_user(**user_data)
        return redirect('user_list')


class AdminUserDetailView(View):
    def get(self, request, user_id):
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/detail.html', {'user': user})

class AdminUserUpdateView(View):
    def get(self, request, user_id):
        choices_gender = [{gender.value: gender.name} for gender in Gender]
        choices_relationship_status = [{status.name: status.value} for status in RelationShipStatus]
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/update.html', {'user': user,"choices_gender":choices_gender,"choices_relationship_status":choices_relationship_status})
    
    def post(self, request, user_id):

        user = services.user_service.get_user(user_id)

        # Gather all form data into a dictionary
        user_data = {
            'first_name': request.POST.get('first_name'),
            'middle_name': request.POST.get('middle_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'hobbies': request.POST.getlist('hobbies'),
            'address': request.POST.get('address'),
            'dob': request.POST.get('dob'),
            'gender': request.POST.get('gender'),
            'relationship_status': request.POST.get('relationship_status'),
        }

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'dob', 'gender', 'address', 'relationship_status']
        for field in required_fields:
            if not user_data.get(field):
                return HttpResponseBadRequest(f"Missing required field: {field}")

        # try:
        #     user_data['dob'] = datetime.fromisoformat(user_data['dob']) 
        # except ValueError:
        #     return HttpResponseBadRequest("Invalid date format for date of birth. Expected format: YYYY-MM-DD")

        # Update the user with the provided data
        services.user_service.update_user(
            user, 
            **user_data  # Pass the dictionary as keyword arguments
        )
        return redirect('user_detail', user_id=user.id)


    # def post(self, request, user_id):
    #     user = services.user_service.get_user(user_id)
    #     first_name = request.POST['first_name']
    #     middle_name = request.POST['middle_name']
    #     last_name = request.POST['last_name']
    #     email = request.POST['email']
    #     hobbies=request.POST.getlist('hobbies')
    #     address=request.POST['address']
    #     dob=request.POST['dob']
    #     gender=request.POST['gender']
    #     relationship_status=request.POST['relationship_status']
    #     services.user_service.update_user(user, first_name,middle_name, last_name, email,hobbies,address,dob,gender,relationship_status)
    #     return redirect('user_detail', user_id=user.id)

class AdminUserDeleteView(View):
    def get(self, request, user_id):
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/delete.html', {'user': user})

    def post(self, request, user_id):
        user = services.user_service.get_user(user_id)
        services.user_service.delete_user(user)
        return redirect('user_list')


class AdminToggleUserActiveView(View):
    def post(self, request, user_id):
        user = services.user_service.get_user(user_id)
        user.is_active = not user.is_active  # Toggle active status
        user.save()
        return JsonResponse({'is_active': user.is_active})



class AdminUserProfileView(View):
    def get(self, request):
        # user = services.user_service.get_user()
        return render(request, 'adminuser/user/user_profile.html')
    


