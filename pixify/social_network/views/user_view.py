from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

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
        return render(request, 'adminuser/user/create.html', {"form": form})

    @catch_error
    def post(self, request):
        form = ManageUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.roles = [2]  # Set default role
            user.save()
            return redirect('user_list')
        return render(request, 'adminuser/user/create.html', {"form": form})

class ManageUserDetailView(View):
    def get(self, request, user_id):
        user = services.manage_user_service.manage_get_user(user_id)
        return render(request, 'adminuser/user/detail.html', {'user': user})
    
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

    @catch_error
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = ManageUserUpdateForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.middle_name = form.cleaned_data.get('middle_name', '')
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()  # Save the updated user instance
            return redirect('user_list')
        return render(request, 'adminuser/user/update.html', {"form": form, "user_id": user.id})

class ManageUserDeleteView(View):
    def get(self, request, user_id):
        user = services.manage_user_service.manage_get_user(user_id)
        return render(request, 'adminuser/user/delete.html', {'user': user})

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

