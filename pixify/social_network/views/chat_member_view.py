from django.shortcuts import redirect
from django.views import View
from ..services import chat_member_service


class MemberManageView(View):
    def post(self, request, chat_id):
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if action == 'add':
            chat_member_service.add_member_to_chat(chat_id, user_id, request.user)
        else:
             chat_member_service.remove_member_from_chat(chat_id, user_id)           

        return redirect('chat_detail', chat_id=chat_id)
