from django.shortcuts import render,redirect
from django.views import View
from ..services import chat_service, user_service

class MessageMentionCreateView(View):
    def get(self,request,chat_id):
        chat=chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
    
    def post(self, request,chat_id):
        user=user_service.get_user(request)
        chat=chat_service.get_chat_by_id(chat_id)
        mention=chat_service.get_all_mentions_by_chat_id(chat,user)
        return render(request, 'enduser/message/index.html',{'mention':mention})