from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from ..services import message_service,user_service, chat_service, message_reaction_service, message_mention_service

class MessageListView(View):
    def get(self, request):
        return render(request, 'enduser/message/index.html')  

class MessageCreateView(View):
    def get(self,request,chat_id):
        chat=chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})  
    
    def post(self, request):        
        text = request.POST['text']
        media_url = request.POST['media_url','']
        sender_id = request.POST['sender_id']
        chat_id = request.POST['chat_id']
        reply_for_message_id=request.POST['reply_for_messages_id']
        mentions= request.POST.getlist('mentions','')
        message = message_service.create_message(text, media_url, sender_id, chat_id, reply_for_message_id)
        for user in mentions:
            message_mention_service.create_message_mentions(message,user)        
        return render(request, 'enduser/message/index.html')

class MessageUpdateView(View):
    def get(self,request,chat_id):
        chat=chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
     
    def post(self, request, message_id):
        message = message_service.get_message_by_id(message_id)        
        text = request.POST['text']
        media_url = request.POST['media_url','']
        message_service.update_message(message, text, media_url)
        return render(request, 'enduser/message/index.html')

class MessageDeleteView(View):  
    def post(self, request, message_id):
        message_service.delete_message(message_id)
        return render(request, 'enduser/message/index.html')
    
class MessageReplyCreateView(View):
    def get(self,request,chat_id):
        chat=chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
    
    def post(self, request, message_id,chat_id):        
        user=user_service.get_user(request)        
        text = request.POST['text']
        media_url = request.POST['media_url','']
        sender_id = user
        chat_id = chat_service.get_chat_by_id(chat_id)
        reply_for_message_id = message_service.get_message_by_id(message_id)         
        mentions=request.POST.getlist('mention','')
        created_by = user
        updated_by = user        
        message_service.reply_message(text,media_url,sender_id,chat_id,reply_for_message_id,created_by,updated_by,mentions)
        for user in mentions:
            message_mention_service.create_message_mentions(message_id,user)
        return render(request, 'enduser/message/index.html')


