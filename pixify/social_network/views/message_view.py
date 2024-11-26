from django.shortcuts import render, redirect
from django.views import View 
from ..models import ChatMember
from ..services import message_service, chat_service, message_mention_service,message_read_status_service, user_service
import re
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class MessageListView(View):
    def get(self, request):
        return render(request, 'enduser/message/index.html')  

class MessageCreateView(View): 
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        chat = chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html', {'chat': chat})
    
    def post(self, request):
        auth_user = request.user
        text = request.POST.get('message')
        chat = chat_service.get_chat_by_id(request.POST.get('chat_id'))
        mentions = request.POST.get('mentions', '')

        print(f"Message: {text}")
        print(f"Mentions: {mentions}")

        mention_ids = []
        if 'all' in mentions.split(','):
            chat_members = ChatMember.objects.filter(chat_id=chat).exclude(member_id=auth_user)
            mention_ids = [member.member_id.id for member in chat_members]
        else:
            mention_ids = [int(id) for id in mentions.split(',') if id.isdigit()]
        
        print(f"Mention IDs: {mention_ids}")

        media_urls = []
        for file in request.FILES.getlist('media_files'):
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)

        message = message_service.create_message(text, media_urls, auth_user, chat)
        print(f"Created Message: {message}")        
        message_read_status_service.create_message_read_status(message,auth_user)
        for user in mention_ids:   
            mentioned_user=user_service.get_user(user)
            message_mention_service.create_message_mentions(message, mentioned_user, auth_user)

        return redirect('chat_details', chat_id=chat.id)

class MessageUpdateView(View): 
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        chat = chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html', {'chat': chat})
 
    def post(self, request, message_id): 
        user = request.user
        message = message_service.get_message_by_id(message_id)
        text = request.POST.get('message', '') 
        media_url = request.POST.get('media_url', '{}')
        mentions = request.POST.get('mentions', '')            

        mention_ids = []

        if mentions == "all":
            chat_members = ChatMember.objects.filter(chat_id=message.chat_id).exclude(member_id=request.user)
            mention_ids = [member.member_id.id for member in chat_members]
        else:
            mention_ids = [int(id) for id in re.split('[, ]+', mentions) if id]
        message_service.update_message(message, text, media_url, user)
        message_mention_service.delete_message_mentions(message,user)
        for mentioned_user in mention_ids:
            message_mention_service.create_message_mentions(message, mentioned_user, user)
        return redirect('chat_details', chat_id=message.chat_id.id)

class MessageDeleteView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    
    def post(self, request, message_id): 
        user = request.user
        message = message_service.get_message_by_id(message_id)
        chat_id = message.chat_id.id
        message_service.delete_message(message, user)
        message_mention_service.delete_message_mentions(message,user)
        return redirect('chat_details', chat_id=chat_id)

class MessageReplyCreateView(View): 
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        chat = chat_service.get_chat_by_id(chat_id)
        return render(request, 'enduser/message/index.html', {'chat': chat})
 
    def post(self, request, message_id):
        auth_user = request.user
        message = message_service.get_message_by_id(message_id)
        text = request.POST.get('message', '')
        media_urls = request.POST.getlist('media_url', '{}')
        chat_id = request.POST.get('chat_id')
        chat = chat_service.get_chat_by_id(chat_id)
        reply_for_message = message
        sender_id=auth_user
        mentions = request.POST.get('mentions', '')
 
        mention_ids = []
        if '@All' in mentions.split(','):
            chat_members = ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=auth_user)
            mention_ids = [member.member_id.id for member in chat_members]
        else:
            mention_ids = [int(id) for id in re.split('[, ]+', mentions) if id.isdigit()]
       
        reply_message=message_service.reply_message(auth_user,text,media_urls,sender_id,chat,reply_for_message)
        message_read_status_service.create_message_read_status(reply_message,auth_user)
        
        for mentioned_user in mention_ids:
            message_mention_service.create_message_mentions(message, mentioned_user, auth_user)
            
        return redirect('chat_details', chat_id=chat.id)