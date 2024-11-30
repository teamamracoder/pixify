from django.shortcuts import redirect,render
from django.views import View
from ..services import chat_member_service
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error


class ChatMemeberCreateView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request,chat_id):        
        return render(request, 'enduser/chat/chats.html',{'chat':chat_id})   
     
    def post(self, request, chat_id):
        members = request.POST.getlist('user_id')     
        for member in members:                              
            chat_member_service.create_chat_member(chat_id, member, request.user)             
        return redirect('chat_detail', chat_id=chat_id)

class ChatMemeberDeleteView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request,chat_id):        
        return render(request, 'enduser/chat/chats.html',{'chat':chat_id})   
     
    def post(self, request, chat_id):
        members = request.POST.getlist('user_id')        
        for member in members:
            chat_member_service.delete_chat_member(chat_id, member, request.user)           

        return redirect('chat_detail', chat_id=chat_id)
    

class ChatMemeberUpdateView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request,chat_id):        
        return render(request, 'enduser/chat/chats.html',{'chat':chat_id})   
     
    def post(self, request, chat_id):       
        return redirect('chat_detail', chat_id=chat_id)    
    