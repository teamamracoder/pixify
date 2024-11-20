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
        auth_user=request.user
        text = request.POST.get('message')
        media_url = request.POST.get('media_url','')
        sender_id = auth_user
        chat = chat_service.get_chat_by_id(request.POST.get('chat_id'))
        message = message_service.create_message(text, media_url, sender_id, chat)
        # error in mention
        # mentions= request.POST.getlist('mentions','[]')
        # print(len(mentions))
        # if len(mentions)>0:    
        #     for user in mentions:
        #         message_mention_service.create_message_mentions(message,user,auth_user)        
        return redirect('chat_details', chat_id=chat.id)
         
class MessageUpdateView(View):
    def get(self,request,chat_id):
        chat=chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html',{'chat':chat})
     
    def post(self, request, message_id):
        message = message_service.get_message_by_id(message_id)        
        text = request.POST['text','']
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


