from django.shortcuts import get_object_or_404, render,redirect
from datetime import timedelta
from django.views import View
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error
from ..services import chat_service, user_service,message_service, chat_member_service,message_reaction_service
from django.http import JsonResponse
from ..constants import ChatType
from django.utils import timezone
import json
from social_network.packages.response import success_response
from social_network.constants.default_values import ResponseMessageType
from social_network.constants.success_messages import SuccessMessage
from social_network.constants.error_messages import ErrorMessage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class ChatListView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        user = request.user
        chats = chat_service.list_chats_by_user(user)
        followers, followings = chat_service.get_all_user_follow(user)
        chat_data = []
        if not chats:
            no_chat_message = {"message": "No chats available"}
            return render(
            request,
            'enduser/chat/chats.html',
            success_response(
                message=request.session.pop("message", ErrorMessage.E000005.value),
                message_type=request.session.pop("message_type", ResponseMessageType.INFO.value),
                data={
                    'no_chats':no_chat_message
                }
            )
        )

        for chat_info in chats:
            chat = chat_info['chat']
            if not chat.id:
                continue

            seen_by_all = chat_info['seen_by_all']
            seen_by_user = chat_info['seen_by_user']
            member = chat_service.members(chat.id)
            latest_reaction = message_reaction_service.latest_reaction(chat, user)
            if member.count() < 2:
                continue
            latest_reaction_type = ''
            if latest_reaction:
                latest_reaction_type = latest_reaction['reaction']
                latest_reaction_message=latest_reaction['reacted_message']
                latest_reaction_message_reacted_by=latest_reaction['reacted_by']
            if not latest_reaction['created_at']:
                latest_reaction['created_at']=chat.latest_message_timestamp - timedelta(hours=1)

            unread_messages = message_service.unread_count(chat, user)
            unread_messages_display = '' if unread_messages == 0 else '10+' if unread_messages > 10 else str(unread_messages)
            if chat.type == ChatType.PERSONAL.value:
                member = chat_service.get_recipient_for_personal(chat.id, user)
                if member:
                    title = f"{member.first_name} {member.last_name}"
                    chat_cover = member.profile_photo_url
                else:
                    title = ''
                    chat_cover = ''
            elif chat.type == ChatType.GROUP.value:
                title = chat.title or chat_service.get_recipients_for_group(chat.id, user)
                chat_cover = chat.chat_cover or ''
            if latest_reaction['created_at'] is not None and latest_reaction['created_at']>chat.latest_message_timestamp:
                latest_message_timestamp =latest_reaction['created_at']
                latest_message=latest_reaction_message
            else:
                latest_message_timestamp = chat.latest_message_timestamp
                latest_message=chat.latest_message
            sender_name=chat_service.latest_message_sender_name(chat.latest_message_sender_id,user.id)
            chat_data.append({
                'user':user,
                'id': chat.id,
                'title': title,
                'chat_cover': chat_cover,
                'latest_message_timestamp':self.format_timestamp(latest_message_timestamp),
                'latest_message':latest_message,
                'unread_messages': unread_messages_display,
                'is_group': chat.type == ChatType.GROUP.value,
                'seen_by_all': seen_by_all,
                'seen_by_user':seen_by_user,
                'latest_reaction_time': latest_reaction['created_at'],
                'latest_reaction': latest_reaction_type,
                'latest_message_time':chat.latest_message_timestamp,
                'latest_reaction_message_reacted_by':latest_reaction_message_reacted_by,
                'latest_message_sender_id':chat.latest_message_sender_id,
                'latest_message_sender_name':sender_name['sender_name']
            })
            print(chat_data)

        return render(
            request,
            'enduser/chat/chats.html',
            success_response(
                message=request.session.pop("message", SuccessMessage.S000013.value),
                message_type=request.session.pop("message_type", ResponseMessageType.INFO.value),
                data={
                    'chats': chat_data,
                }
            )
        )
    def format_timestamp(self, timestamp):
        if not timestamp:
            return ''
        now = timezone.now()
        diff = now - timestamp
        if diff.days == 0:
            return timestamp.strftime('%I:%M %p')
        elif diff.days == 1:
            return 'Yesterday'
        elif diff.days < 7:
            return timestamp.strftime('%A')
        else:
            return timestamp.strftime('%d/%m/%Y')


class ChatCreateView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        user = user_service.get_user(request)
        return render(request, 'enduser/chat/chats.html',{'user':user})

    def post(self, request):
        user = request.user
        data = json.loads(request.body.decode('utf-8'))
        chat_type = int(data.get('type'))
        members = data.get('members', [])

        if chat_type == ChatType.PERSONAL.value:

            member = members[0]
            existing_chat = chat_service.get_existing_personal_chat(chat_type,user.id, member)
            if existing_chat:

                return JsonResponse({
                    'chat_id': existing_chat.id,
                    'message':SuccessMessage.S000008.value
                    }
                )

            chat = chat_service.create_chat(user, None, None, ChatType.PERSONAL.value)
            chat_member_service.add_chat_member(chat.id, user.id, user)
            chat_member_service.add_chat_member(chat.id, member, user)

            return JsonResponse({
                'chat_id': chat.id,
                'message':SuccessMessage.S000007.value
                }
            )

        elif chat_type == ChatType.GROUP.value:

            title = data.get('title', '')
            chat_cover = data.get('chat_cover', '')
            chat = chat_service.create_chat(user, title, chat_cover, chat_type)
            members.append(user.id)
            for member in members:
                chat_member_service.add_chat_member(chat.id, member, user)

            # return JsonResponse({'chat_id': chat.id})
            return JsonResponse({
                'chat_id': chat.id,
                'message':SuccessMessage.S000007.value
                }
            )

class ChatDetailsView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, chat_id):
        user = request.user
        chat = chat_service.chat_details(chat_id,user.id)
        return render(
            request,
            'enduser/chat/chat_details.html',
            success_response(
                message=request.session.pop("message", SuccessMessage.S000007.value),
                message_type=request.session.pop("message_type", ResponseMessageType.INFO.value),
                data={
                    'chat': chat,
                    'user':user,
                }
            )
        )


class ChatUpdateView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, chat_id):
        try:
            user = request.user
            chat = chat_service.get_chat_by_id(chat_id)

            # Parse JSON data from the request body
            if 'application/json' in request.content_type:
                data = json.loads(request.body)
                title = data.get('title', None)  # Safely get the title
                if title:
                    chat_service.update_chat_title(chat, title, user)
                if 'chat_bio' in data:
                    chat_service.update_chat_bio(chat, data['chat_bio'], user)

            # Handle file upload separately
            if 'multipart/form-data' in request.content_type:
                chat_cover = request.FILES.get('chat_cover', None)
                if chat_cover:
                    file_name = default_storage.save(chat_cover.name, ContentFile(chat_cover.read()))
                    media_url = default_storage.url(file_name)
                    chat_service.update_chat_cover(chat, media_url, user)

            return JsonResponse({"success": True, "message": "Chat updated successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


class ChatDeleteView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, chat_id):
        user = request.user
        members = chat_member_service.get_chat_members(chat_id)
        for member in members:
            chat_member_service.delete_chat_member(chat_id, member, user)
        chat_service.delete_chat(chat_id)
        return JsonResponse({"success": True})

class ChatListViewApi(View):
    def get(self, request):
        user = request.user
        chats = chat_service.list_chats_by_user_api(user)
        chat_data_list = []
        for chat in chats:
            if chat.type == ChatType.PERSONAL.value:
                member = chat_service.get_recipient_for_personal(chat.id, user)
                title = f"{member.first_name} {member.last_name}"
                chat_cover = member.profile_photo_url or '/static/images/avatar.jpg'
                chat_info = {
                    'id': chat.id,
                    'title': title,
                    'chat_cover': chat_cover,
                }
            elif chat.type == ChatType.GROUP.value:
                title = chat.title or chat_service.get_recipients_for_group(chat.id, user)
                chat_cover = chat.chat_cover or '/static/images/group_pic.png'
                chat_info = {
                    'id': chat.id,
                    'title': title,
                    'chat_cover': chat_cover,
                }
            chat_data_list.append(chat_info)

            filtered_chats = chat_service.list_chats_api(request,chat_data_list)
        # Return the (filtered) list of chats.
        return JsonResponse(filtered_chats, safe=False)

