from django.shortcuts import redirect,render
from django.views import View
from ..services import chat_member_service
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error
from django.http import JsonResponse
import json


class ChatMemeberCreateView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):        
        return render(request, 'enduser/chat/chats.html', {'chat': chat_id})   
     
    def post(self, request, chat_id):
        try:
            data = json.loads(request.body)
            member_ids = data.get('member_ids') 

            for member_id in member_ids:
                chat_member_service.add_chat_member(chat_id, member_id, request.user)

            return JsonResponse({"success": True, "message": "Members added successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class ChatMemeberDeleteView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):        
        return render(request, 'enduser/chat/chats.html', {'chat': chat_id})   
     
    def post(self, request, chat_id):
        try:
            data = json.loads(request.body)
            member = data.get('member_id')
            
            if isinstance(member, str):
                try:
                    member_id = int(member.split(',')[0].split(':')[1].strip())
                except (ValueError, IndexError):
                    return JsonResponse({"success": False, "message": "Invalid member ID format"}, status=400)
            elif isinstance(member, int):
                member_id = member
            else:
                return JsonResponse({"success": False, "message": "Invalid member ID type"}, status=400)
                
            chat_member_service.delete_chat_member(chat_id, member_id, request.user)  
            return JsonResponse({"success": True, "message": "Chat updated successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)



class ChatMemeberUpdateView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request,chat_id):        
        return render(request, 'enduser/chat/chats.html',{'chat':chat_id})   
     
    def post(self, request, chat_id):       
        return redirect('chat_detail', chat_id=chat_id)    
    