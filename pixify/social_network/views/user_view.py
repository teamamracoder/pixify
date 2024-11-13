from django.shortcuts import render, redirect
from django.views import View
from .. import services
from ..constants import Gender, RelationShipStatus, Role

class UserListView(View):
    def get(self, request):
        
        users = services.user_service.list_users()
        return render(request, 'adminuser/user/list.html', {'users': users})

class UserCreateView(View):
    def get(self, request):
        choices_gender = [{gender.value: gender.name} for gender in Gender]
        choices_relationship_status = [{status.name: status.value} for status in RelationShipStatus]
        return render(request, 'adminuser/user/create.html',{"choices_gender":choices_gender,"choices_relationship_status":choices_relationship_status})

    def post(self, request):
        print(request)
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address=request.POST['address']
        dob=request.POST['dob']
        gender=request.POST['gender']
        relationship_status=request.POST['relationship_status']
        hobbies=request.POST.getlist('hobbies')
        services.user_service.create_user(first_name,middle_name, last_name, email,address,dob,gender,relationship_status,hobbies)
        return redirect('user_list')

class UserDetailView(View):
    def get(self, request, user_id):
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/detail.html', {'user': user})

class UserUpdateView(View):
    def get(self, request, user_id):
        choices_gender = [{gender.value: gender.name} for gender in Gender]
        choices_relationship_status = [{status.name: status.value} for status in RelationShipStatus]
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/update.html', {'user': user,"choices_gender":choices_gender,"choices_relationship_status":choices_relationship_status})

    def post(self, request, user_id):
        user = services.user_service.get_user(user_id)
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        hobbies=request.POST.getlist('hobbies')
        address=request.POST['address']
        dob=request.POST['dob']
        gender=request.POST['gender']
        relationship_status=request.POST['relationship_status']
        services.user_service.update_user(user, first_name,middle_name, last_name, email,hobbies,address,dob,gender,relationship_status)
        return redirect('user_detail', user_id=user.id)

class UserDeleteView(View):
    def get(self, request, user_id):
        user = services.user_service.get_user(user_id)
        return render(request, 'adminuser/user/delete.html', {'user': user})

    def post(self, request, user_id):
        user = services.user_service.get_user(user_id)
        services.user_service.delete_user(user)
        return redirect('user_list')
