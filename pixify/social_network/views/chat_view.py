from django.shortcuts import render,redirect
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
                message=request.session.pop("message", SuccessMessage.S000009.value),
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
            member = chat_service.count_members(chat.id)
            latest_reaction = message_reaction_service.latest_reaction(chat, user)
            if member.count() < 2:
                continue  
            latest_reaction_timestamp = ''
            latest_reaction_type = ''
            if latest_reaction:
                latest_reaction_timestamp = self.format_timestamp(latest_reaction['created_at'])
                latest_reaction_type = latest_reaction['reaction']
                latest_reaction_message=latest_reaction['reacted_message']
                latest_reaction_message_reacted_by=latest_reaction['reacted_by']

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

            latest_message_timestamp = self.format_timestamp(chat.latest_message_timestamp)
            chat_data.append({
                'id': chat.id,
                'title': title,
                'chat_cover': chat_cover,
                'latest_message_timestamp': latest_message_timestamp,
                'latest_message': chat.latest_message,
                'unread_messages': unread_messages_display,
                'is_group': chat.type == ChatType.GROUP.value,
                'seen_by_all': seen_by_all,
                'latest_reaction_timestamp': latest_reaction_timestamp,
                'latest_reaction': latest_reaction_type,
                'latest_reaction_message':latest_reaction_message,
                'latest_reaction_message_reacted_by':latest_reaction_message_reacted_by
            })

        follow_data = []
        for follower in followers:
            follow_data.append({
                'title': f"{follower.following.first_name} {follower.following.last_name}",
                'photo': follower.following.profile_photo_url,
            })
        for following in followings:
            follow_data.append({
                'title': f"{following.follower.first_name} {following.follower.last_name}",
                'photo': following.follower.profile_photo_url,
            })
        return render(
            request,
            'enduser/chat/chats.html',
            success_response(
                message=request.session.pop("message", SuccessMessage.S000007.value),
                message_type=request.session.pop("message_type", ResponseMessageType.INFO.value),
                data={
                    'chats': chat_data,
                    'follow': follow_data
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
                return JsonResponse({'chat_id': existing_chat.id})

            chat = chat_service.create_chat(user, None, None, ChatType.PERSONAL.value)
            chat_member_service.create_chat_member(chat.id, user.id, user)
            chat_member_service.create_chat_member(chat.id, member, user)
            return JsonResponse({'chat_id': chat.id})

        elif chat_type == ChatType.GROUP.value:
            title = data.get('title', '')
            chat_cover = data.get('chat_cover', '')
            chat = chat_service.create_chat(user, title, chat_cover, chat_type)
            members.append(user.id)
            for member in members:
                chat_member_service.create_chat_member(chat.id, member, user)

            return JsonResponse({'chat_id': chat.id})
 
class ChatDetailsView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request,chat_id):        
        return render(request, 'enduser/chat/chats.html',{'chat':chat_id})  
    
        



class ChatUpdateView(View):   
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request,chat_id):        
        return render(request, 'enduser/chat/chats.html',{'chat':chat_id})   
     
    def post(self,request,chat_id):
        user=request.user
        chat  = chat_service.get_chat_by_id(chat_id)
        title = request.POST['titel','']        
        chat_cover = request.POST.get('chat_cover', '')                
        chat_service.update_chat(chat, title, chat_cover, user)                  
        return redirect('chat/')

class ChatDeleteView(View):  
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, chat_id):
        chat = chat_service.get_chat_by_id(chat_id)
        chat_service.delete_chat(chat)
        return redirect('chat_list')

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
                if chat_cover:
                    chat_info = {
                        'id': chat.id,
                        'title': title,
                        'chat_cover': chat_cover,
                    }
                else:
                    chat_info = {
                        'id': chat.id,
                        'title': title,
                        'chat_cover': '/static/images/avatar.jpg',
                    } 
            elif chat.type == ChatType.GROUP.value:
                title = chat.title or chat_service.get_recipients_for_group(chat.id, user)
                chat_cover = chat.chat_cover or '/static/images/group_pic.png'
                if chat_cover:
                    chat_info = {
                        'id': chat.id,
                        'title': title,
                        'chat_cover': chat_cover,
                    }
                else:
                    chat_info = {
                        'id': chat.id,
                        'title': title,
                        'chat_cover':'/static/images/group_pic.png',
                    } 
            chat_data_list.append(chat_info)
        chats = chat_service.list_chats_api(request,chat_data_list)
        return JsonResponse(chats, safe=False)