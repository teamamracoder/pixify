from django.shortcuts import render, redirect
from django.views import View
from ..models import ChatMember,User
from ..services import message_service, chat_service, message_mention_service,message_read_status_service, user_service,message_reaction_service 
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import ChatType, ResponseMessageType, Role
from ..decorators import auth_required, role_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ..constants import ChatType
from social_network.constants.success_messages import SuccessMessage
from collections import defaultdict
from social_network.packages.response import success_response

class MessageListView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        user = request.user
        chat = chat_service.get_chat_by_id(chat_id)
        reactions = message_reaction_service.show_reactions()
        messages = message_service.list_messages_by_chat_id(chat_id, user.id)

        # Check if each message is editable (within the last 10 minutes)
        for message in messages:
            message.is_editable = message_service.is_editable(message)
        # Check if each message has been seen by all members        
            message.seen_by_all = chat_service.is_message_seen_by_all(message)
        # Apply the timestamp formatting function to each message        
            message.formatted_timestamp = message_service.format_timestamp(message.created_at)

        # Group the messages by their formatted timestamp
        grouped_messages = defaultdict(list)                

        for message in messages:            
            grouped_messages[message.formatted_timestamp].append(message)

        # Convert defaultdict to a list of tuples to make it easier to iterate in the template
        grouped_messages_list = [(date, sorted(messages, key=lambda x: x.created_at)) if date == 'Today' else (date, messages) for date, messages in grouped_messages.items()]
        
        # Sort grouped messages based on the custom sort key
        grouped_messages_list = sorted(grouped_messages_list, key=lambda x: message_service.sort_key(x)[0])   

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
            'type':chat.type,
            'chat_cover': chat_cover,
            'is_group': chat.type == ChatType.GROUP.value,
            'seen_by_all': seen_by_all  # This is for the latest message
        }

        return render(request, 'enduser/chat/messages.html',
            success_response(               
            message=request.session.pop("message", SuccessMessage.S000014.value),
            message_type=request.session.pop(
            "message_type", ResponseMessageType.INFO.value
        ),
            data={ 
            'chat': chat_info,
            'grouped_messages':grouped_messages_list,
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

        # Store the success message in the session 
        request.session['success_message'] = SuccessMessage.S000014.value
        
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

        message_service.update_message(message, text, media_urls, user)

        for mentioned_user in removed_mentions:
            mentioned_user_instance = user_service.get_user(mentioned_user)
            message_mention_service.delete_message_mentions(message, user, [mentioned_user_instance])

        for mentioned_user in added_mentions:
            mentioned_user_instance = user_service.get_user(mentioned_user)
            message_mention_service.create_message_mentions(message, mentioned_user_instance, user)
        
        request.session['success_message'] = SuccessMessage.S000010.value
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

        for mentioned_user in current_mentions:            
            mentioned_user_instance = user_service.get_user(mentioned_user.user_id)
            message_mention_service.delete_message_mentions(message, auth_user, [mentioned_user_instance])   

        message_service.delete_message(message, auth_user)  

        request.session['success_message'] = SuccessMessage.S000011.value
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

        request.session['success_message'] = SuccessMessage.S000012.value            
        return redirect('message', chat_id=chat.id)
