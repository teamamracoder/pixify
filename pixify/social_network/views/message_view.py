from django.shortcuts import render, redirect
from django.views import View

from social_network.packages.response import success_response
from social_network.constants.default_values import ResponseMessageType
from social_network.constants.success_messages import SuccessMessage

from ..models import ChatMember
from ..services import message_service, chat_service, message_mention_service,message_read_status_service, user_service,message_reaction_service 
import re
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import ChatType, ResponseMessageType, Role
from ..decorators import auth_required, role_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class MessageListView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        user = request.user
        chat = chat_service.get_chat_by_id(chat_id)
        reactions = message_reaction_service.show_reactions()
        messages = message_service.list_messages_by_chat_id(chat_id, user.id)

        # Check if each message has been seen by all members
        for message in messages:
            message.seen_by_all = chat_service.is_message_seen_by_all(message)

        latest_message = message_service.get_latest_message(chat.id)
        seen_by_all = False

        if latest_message:
            seen_by_all = chat_service.is_message_seen_by_all(latest_message)

        if chat.type == ChatType.PERSONAL.value:
            member = chat_service.get_recipient_for_personal(chat.id, user)
            if member:
                title = f"{member.first_name} {member.last_name}"
                chat_cover = member.profile_photo_url
            else:
                title = ''
                chat_cover = ''
        elif chat.type == ChatType.GROUP.value:
            title = chat_service.get_recipients_for_group(chat.id, user)
            if chat.title:
                title = chat.title
            if chat.chat_cover:
                chat_cover = chat.chat_cover
            else:
                chat_cover = ''

        chat_info = {
            'id': chat.id,
            'title': title,
            'chat_cover': chat_cover,
            'is_group': chat.type == ChatType.GROUP.value,
            'seen_by_all': seen_by_all  # This is for the latest message
        }

        return render(request, 'enduser/chat/messages.html',
            success_response(               
            message=request.session.pop("message", SuccessMessage.S000008.value),
            message_type=request.session.pop(
            "message_type", ResponseMessageType.INFO.value
        ),
            data={ 
            'chat': chat_info,
            'messages': messages,
            'user': user,
            'reactions': reactions
        }
        ))

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
        mention_ids = []
        if 'all' in mentions.split(','):

            chat_members = ChatMember.objects.filter(chat_id=chat).exclude(member_id=auth_user)
            mention_ids = [member.member_id.id for member in chat_members]
        else:
            mention_ids = [int(id) for id in mentions.split(',') if id.isdigit()]
        media_urls = []
        for file in request.FILES.getlist('media_files'):
            file_name = default_storage.save(file.name, ContentFile(file.read()))
            media_url = default_storage.url(file_name)
            media_urls.append(media_url)

        message = message_service.create_message(text, media_urls, auth_user, chat)  
        message_read_status_service.create_message_read_status(message,auth_user)
        for user in mention_ids:   
            mentioned_user=user_service.get_user(user)
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