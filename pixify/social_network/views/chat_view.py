from django.shortcuts import render,redirect
from django.views import View
from django.utils import timezone
from django.utils.timezone import localtime
from ..models import Message, ChatMember, Follower
from ..services import chat_service, user_service,message_service
from ..constants import ChatType


class ChatListView(View):
    def get(self, request):
        chats = chat_service.list_chats()  
        user = user_service.get_user(1)  
        chat_data = []  
        for chat in chats:
            chat_info = {}
            chat_members = ChatMember.objects.filter(chat_id=chat.id).exclude(member_id=user.id).select_related('member_id').first()  
            if not chat_members:
                continue  
            if chat.type == ChatType.GROUP.value:
                chat_info = {
                    'title': chat.title,  
                    'photo': chat.chat_cover, 
                }
            elif chat.type == ChatType.PERSONAL.value:
                if chat_members:
                    member = chat_members.member_id
                    chat_info = {
                        'title': f"{member.first_name} {member.last_name}",  
                        'photo': member.profile_photo_url,  
                    }
                else:
                    chat_info = {
                        'title': "Unknown",  
                        'photo': None  
                    }
            last_message = Message.objects.filter(chat_id=chat.id).order_by('-send_at').first()
            if last_message:
                last_message_time = last_message.send_at
                chat_info['last_message'] = last_message 
                chat_info['last_message_time'] = self.format_message_time(last_message_time)  
            else:
                chat_info['last_message'] = None  
            unread_count = self.get_unread_message_count(user.id, chat.id)
            if unread_count == 0:
                chat_info['unread_count'] = None  
            elif unread_count > 10:
                chat_info['unread_count'] = '10+' 
            else:
                chat_info['unread_count'] = unread_count
            chat_data.append(chat_info)
        user_id = user.id  
        followers = Follower.objects.filter(following=user_id).exclude(follower=user_id).select_related('follower')
        followings = Follower.objects.filter(follower=user_id).exclude(following=user_id).select_related('following')
        follow_data = []  
        for follower in followers:
            follow_data.append({
                'title': f"{follower.follower.first_name} {follower.follower.last_name}",
                'photo': follower.follower.profile_photo_url,
            })
        for following in followings:
            follow_data.append({
                'title': f"{following.following.first_name} {following.following.last_name}",
                'photo': following.following.profile_photo_url,
            })
            
        print(follow_data)
        return render(request, 'enduser/chat/chats.html', {
            'chats': chat_data,
            'follow_data': follow_data  
        })
    def get_unread_message_count(self, user_id, chat_id):
        return Message.objects.filter(
            chat_id=chat_id, 
            is_read=False,  
            receiver_id=user_id 
        ).count()
    def format_message_time(self, timestamp):     
        now = localtime(timezone.now())
        time_diff = now - timestamp
        if time_diff.days == 0: 
            return timestamp.strftime('%H:%M') 
        elif time_diff.days == 1: 
            return f"Yesterday {timestamp.strftime('%H:%M')}"   
        else: 
            return timestamp.strftime('%Y-%m-%d %H:%M')



class ChatCreateView(View):
    def post(self, request, user_id):
        data = chat_service.get_user_data(user_id)
        if 'followers' not in data or 'followings' not in data:
            return redirect('error_page') 
        return render(request, 'enduser/chat/user_profile.html', {
            'title': 'User Followers and Following',
            'photo': data['photo'],
            'followers': data['followers'],
            'followings': data['followings'],
        })



class ChatDetailsView(View):
    def get(self, request, chat_id):
        chat = chat_service.get_chat(chat_id)
        messages = message_service.list_messages_by_chat_id(chat_id)
        return render(request, 'enduser/chat/messages.html',{'chat':chat,'messages':messages})

    def post(self, request, chat_id):
        chat = chat_service.get_chat(chat_id)
        chat_service.delete_chat(chat)
        return redirect('chat_list')


class ChatUpdatesView(View):
    def get(self, request, chat_id):
        chat = chat_service.details_chats(chat_id)
        messages = message_service.list_messages_by_chat_id(chat_id)
        return 

    def post(self, request, chat_id):
        chat = chat_service.get_chat(chat_id)
        chat_service.delete_chat(chat)
        return redirect('chat_list')


class ChatDeleteView(View):
    def get(self, request, chat_id):
        chat = chat_service.details_chats(chat_id)
        messages = message_service.list_messages_by_chat_id(chat_id)
        return

    def post(self, request, chat_id):
        chat = chat_service.get_chat(chat_id)
        chat_service.delete_chat(chat)
        return redirect('chat_list')