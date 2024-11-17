from django.shortcuts import render, redirect
from django.views import View
from ..services import message_service, user_service, chat_service

class messageView(View):
    def get(self, request):
        return render(request, 'enduser/message/index.html')  

class messageCreateView(View):
    def post(self,request,chat_id):
        chat=chat_service.chat_details(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})  
    
    def get(self, request):        
        text = request.POST['text']
        media_url = request.POST['media_url','']
        sender_id = request.POST['sender_id']
        chat_id = request.POST['chat_id']
        reply_for_message_id=request.POST['reply_for_messages_id']
        mentions= request.POST.getlist('mentions','')
        message_service.create_message(text, media_url, sender_id, chat_id, reply_for_message_id)
        for user in mentions:
            message_service.add_message_mentions(message_id,user)        
        return render(request, 'enduser/message/index.html')

class messageUpdateView(View):
    def post(self,request,chat_id):
        chat=chat_service.chat_details(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
     
    def get(self, request, message_id):
        message = message_service.get_message(message_id)        
        text = request.POST['text']
        media_url = request.POST['media_url','']
        message_service.update_message(message, text, media_url)
        return render(request, 'enduser/message/index.html')

class messageDeleteView(View):
    def post(self,request,chat_id):
        chat=chat_service.chat_details(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
    
    def get(self, request, message_id):
        message_service.delete_message(message_id)
        return render(request, 'enduser/message/index.html')
    
class messageMentionView(View):
    def post(self,request,chat_id):
        chat=chat_service.chat_details(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
    
    def get(self, request,chat_id):
        user=user_service.get_user(request)
        chat=chat_service.get_chat(chat_id)
        mention=chat_service.mention_chat(chat,user)
        return render(request, 'enduser/message/index.html',{'mention':mention})
    
class messageReplyView(View):
    def post(self,request,chat_id):
        chat=chat_service.chat_details(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
    
    def get(self, request, message_id,chat_id):        
        user=user_service.get_user(request)        
        text = request.POST['text']
        media_url = request.POST['media_url','']
        sender_id = user
        chat_id = chat_service.chat_details(chat_id)
        reply_for_message_id = message_service.get_message(message_id)         
        mentions=request.POST.getlist('mention','')
        created_by = user
        updated_by = user        
        message_service.reply_message(text,media_url,sender_id,chat_id,reply_for_message_id,created_by,updated_by,mentions)
        for user in mentions:
            message_service.add_message_mentions(message_id,user)
        return render(request, 'enduser/message/index.html')