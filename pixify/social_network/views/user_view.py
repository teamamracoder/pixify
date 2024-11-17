from django.shortcuts import render, redirect
from django.views import View
from .. import services
from django.http import JsonResponse

class UserListView(View):
    def get(self, request):
        users = services.user_service.list_users()
        return render(request, 'adminuser/user/list.html', {'users': users})

class UserCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/user/create.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        services.user_service.create_user(first_name, last_name, email)
        return redirect('user_list')

class UserDetailView(View):
    def get(self, request, user_id):
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/detail.html', {'user': user})

class UserUpdateView(View):
    def get(self, request, user_id):
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/update.html', {'user': user})

    def post(self, request, user_id):
        user = services.user_service.get_user(user_id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        services.user_service.update_user(user, first_name, last_name, email)
        return redirect('user_detail', user_id=user.id)

class UserDeleteView(View):
    def get(self, request, user_id):
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/delete.html', {'user': user})

    def post(self, request, user_id):
        user = services.user_service.get_user(user_id)
        services.user_service.delete_user(user)
        return redirect('user_list')