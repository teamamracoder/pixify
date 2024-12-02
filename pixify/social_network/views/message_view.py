from django.shortcuts import render, redirect
from django.views import View 
from ..models import ChatMember,User
from ..services import message_service, chat_service, message_mention_service,message_read_status_service, user_service
import re
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..constants import ChatType

class MessageListView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        user =request.user 
        chat = chat_service.get_chat_by_id(chat_id)
        messages = message_service.list_messages_by_chat_id(chat_id,user.id)
        if chat.type == ChatType.PERSONAL.value:
            member = chat_service.get_recipient_for_personal(chat.id, user) 
            if member:
                title = f"{member.first_name} {member.last_name}"
                chat_cover = member.profile_photo_url
            else:
                title = ''
                chat_cover=''
        elif chat.type == ChatType.GROUP.value:
            title= chat_service.get_recipients_for_group(chat.id,user)
            if chat.title:    
                title = chat.title 
            else:
                title=title 
            if chat.chat_cover:
                chat_cover=chat.chat_cover
            else:
                chat_cover=''            
        chat_info = {
            'id': chat.id,
            'title': title,
            'chat_cover': chat_cover,
            'is_group' :chat.type==ChatType.GROUP.value,
            'type':chat.type
        }
        # chat_data.append(chat_info)       
        return render(request, 'enduser/chat/messages.html',{'chat':chat_info,'messages':messages,'user':user})
     

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
        mentions = request.POST.get('mentions','')       
        mention_list = mentions.split(',')  # Split mentions into individual names       
        mention_ids = []

        numeric_ids = [id for id in mention_list if id.isdigit()]
        mention_ids = numeric_ids[:]

        for username in mention_list:
            username = username.strip()
            if username.lower() == 'all': 
                chat_members = ChatMember.objects.filter(chat_id=chat).exclude(member_id=auth_user)
                mention_ids.extend(member.member_id.id for member in chat_members)
            else:
                user_obj = User.objects.filter(first_name__iexact=username).first()
                if user_obj:
                    mention_ids.append(user_obj.id)

        print(mention_ids)        
        media_urls = []
        for file in request.FILES.getlist('media_files'):
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)
        
        message = message_service.create_message(text, media_urls, auth_user, chat)  
        message_read_status_service.create_message_read_status(message, auth_user)
        
        for user in mention_ids:
            mentioned_user = user_service.get_user(user)
            message_mention_service.create_message_mentions(message, mentioned_user, auth_user)
        
        return redirect('message', chat_id=chat.id)

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
        media_urls = []
        for file in request.FILES.getlist('media_files'):
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)
        
        mentions = request.POST.get('mentions', '')
        mention_list = mentions.split(',')       
        mention_ids = []

        numeric_ids = [id for id in mention_list if id.isdigit()]
        mention_ids = numeric_ids[:]

        for username in mention_list:
            username = username.strip()
            if username.lower() == 'all': 
                chat_members = ChatMember.objects.filter(chat_id=message.chat_id).exclude(member_id=user)
                mention_ids.extend(member.member_id.id for member in chat_members)
            else:
                user_obj = User.objects.filter(first_name__iexact=username).first()
                if user_obj:
                    mention_ids.append(user_obj.id)

        current_mentions = message_mention_service.get_message_mentions(message)
        current_mention_ids = set(current_mentions.values_list('user_id', flat=True))

        new_mention_ids = set(mention_ids)
        removed_mentions = current_mention_ids - new_mention_ids
        added_mentions = new_mention_ids - current_mention_ids

        print(new_mention_ids)
        print(removed_mentions)
        print(added_mentions)
        print(message)

        message_service.update_message(message, text, media_urls, user)

        for mentioned_user in removed_mentions:
            mentioned_user_instance = user_service.get_user(mentioned_user)
            message_mention_service.delete_message_mentions(message, user, [mentioned_user_instance])

        for mentioned_user in added_mentions:
            mentioned_user_instance = user_service.get_user(mentioned_user)
            message_mention_service.create_message_mentions(message, mentioned_user_instance, user)
        
        return redirect('message', chat_id=message.chat_id.id)


class MessageDeleteView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    
    def post(self, request, message_id): 
        auth_user = request.user
        message = message_service.get_message_by_id(message_id)
        chat_id = message.chat_id.id        
        current_mentions = message_mention_service.get_message_mentions(message.id)

        print("hiiiiiiiiiii")
        print(current_mentions)

        for mentioned_user in current_mentions:            
            mentioned_user_instance = user_service.get_user(mentioned_user.user_id)
            message_mention_service.delete_message_mentions(message, auth_user, [mentioned_user_instance])   

        message_service.delete_message(message, auth_user)  
        return redirect('message', chat_id=chat_id)

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
        
        media_urls = []
        for file in request.FILES.getlist('media_files'):
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)
        
        chat_id = request.POST.get('chat_id')
        chat = chat_service.get_chat_by_id(chat_id)
        reply_for_message = message
        mentions = request.POST.get('mentions', '')

        mention_list = mentions.split(',')
        mention_ids = []

        if '@All' in mention_list:
            chat_members = ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=auth_user)
            mention_ids.extend([member.member_id.id for member in chat_members])
        else:
            mention_ids.extend([int(id) for id in mention_list if id.isdigit()])

        reply_message = message_service.reply_message(auth_user, text, media_urls, auth_user, chat, reply_for_message)
        message_read_status_service.create_message_read_status(reply_message, auth_user)
        
        for mentioned_user in mention_ids:
            mentioned_user_instance = user_service.get_user(mentioned_user)
            message_mention_service.create_message_mentions(reply_message, mentioned_user_instance, auth_user)
            
        return redirect('message', chat_id=chat.id)
