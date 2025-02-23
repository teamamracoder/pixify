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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string


class MessageListView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        user = request.user
        chat = chat_service.get_chat_by_id(chat_id)
        reactions = message_reaction_service.show_reactions()
        messages = message_service.list_messages_by_chat_id(chat_id, user.id)

        # Process each message.
        for message in messages:
            message.is_editable = message_service.is_editable(message)
            message.seen_by_all = chat_service.is_message_seen_by_all(message)
            message.seen_by_user = chat_service.is_message_seen_by_user(message, user)

            message.formatted_timestamp = message_service.format_timestamp(message.created_at)
            
            # Retrieve the reaction data for this message.
            msg_reaction = message_reaction_service.reaction_by_message_id(message.id)

            if msg_reaction:
                # Create a dictionary keyed by reaction_id for counts.
                message.msg_reaction_count = {
                    item['reaction_id']: item['count'] for item in msg_reaction
                }
                # Create a dictionary keyed by reaction_id for react_value.
                message.msg_reaction_value = {
                    item['reaction_id']: item['react_value'] for item in msg_reaction
                }
            else:
                message.msg_reaction_count = {}
                message.msg_reaction_value = {}
        
        # Group all messages by formatted timestamp.
        all_grouped_messages = defaultdict(list)
        for message in messages:
            all_grouped_messages[message.formatted_timestamp].append(message)
        grouped_messages_list = [
            (date, sorted(msg_list, key=lambda x: x.created_at))
            for date, msg_list in all_grouped_messages.items()
        ]
        grouped_messages_list = sorted(grouped_messages_list, key=lambda x: message_service.sort_key(x)[0])

        # Determine seen status for the latest message.
        latest_message = message_service.get_latest_message(chat.id)
        seen_by_all = chat_service.is_message_seen_by_all(latest_message) if latest_message else False

        # Set up pagination (10 messages per page).
        per_page = 20
        paginator = Paginator(messages, per_page)
        page_param = request.GET.get('page')
        if page_param:
            try:
                page = int(page_param)
            except ValueError:
                page = paginator.num_pages
        else:
            page = paginator.num_pages

        try:
            messages_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            messages_page = paginator.page(paginator.num_pages)

        # Group only the messages on the current page.
        current_grouped = defaultdict(list)
        for message in messages_page:
            current_grouped[message.formatted_timestamp].append(message)
        grouped_messages_current = [
            (date, sorted(msg_list, key=lambda x: x.created_at))
            for date, msg_list in current_grouped.items()
        ]
        grouped_messages_current = sorted(grouped_messages_current, key=lambda x: message_service.sort_key(x)[0])

        # Prepare chat info.
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
            chat_cover = chat.chat_cover if chat.chat_cover else ''

        chat_info = {
            'id': chat.id,
            'title': title,
            'type': chat.type,
            'chat_cover': chat_cover,
            'is_group': chat.type == ChatType.GROUP.value,
            'seen_by_all': seen_by_all,
        }

        # --- AJAX branch for older messages ---
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Get the last_timestamp passed from the client.
            last_timestamp = request.GET.get('last_timestamp')
            duplicate_timestamp = False
            if last_timestamp and grouped_messages_current:
                if grouped_messages_current[0][0] == last_timestamp:
                    duplicate_timestamp = True

            html = render_to_string(
                'enduser/chat/messages_list_partial.html',
                {
                    'grouped_messages': grouped_messages_current,
                    'messages': messages_page,
                    'current_page': messages_page.number,
                    'has_previous': messages_page.has_previous(),
                    'reactions': reactions,
                    'duplicate_timestamp': duplicate_timestamp,                    
                },
                request=request
            )
            return JsonResponse({'html': html, 'current_page': messages_page.number})
        else:
            # For a full-page load.
            return render(
                request,
                'enduser/chat/messages.html',
                {
                    'data': {
                        'chat': chat_info,
                        'grouped_messages': grouped_messages_current,
                        'messages': messages_page,
                        'user': user,
                        'reactions': reactions,
                        'paginator': paginator,
                        'current_page': messages_page.number,                        
                    },
                    'message': request.session.pop("message", SuccessMessage.S000014.value),
                    'message_type': request.session.pop("message_type", ResponseMessageType.INFO.value),
                }
            )







         

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
