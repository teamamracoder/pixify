from django.shortcuts import redirect
from django.views import View
from ..services import chat_member_service


class ChatMemeberUpdateView(View):
    def post(self, request, chat_id):
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if action == 'add':
            chat_member_service.create_chat_member(chat_id, user_id, request.user)
        else:
            chat_member_service.delete_chat_member(chat_id, user_id, request.user)           

        return redirect('chat_detail', chat_id=chat_id)
