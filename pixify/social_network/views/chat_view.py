from django.shortcuts import render,redirect
from django.views import View
from ..services import chat_service, user_service,message_service
from django.http import JsonResponse
from ..constants import ChatType
from django.utils import timezone
from django.shortcuts import render

class ChatListView(View):
    def get(self, request):
        user = user_service.get_user(2)
        chats = chat_service.list_chats(user)
        followers, followings = chat_service.user_follow(user)
        chat_data = []

        for chat in chats:
            unread_messages = message_service.unread_count(chat, user)
            unread_messages_display = '' if unread_messages == 0 else '4+' if unread_messages > 4 else str(unread_messages)

            if not chat.latest_message:
                chat.latest_message = ''

            member = chat_service.chat_member(chat.id, user)
            if chat.type == ChatType.PERSONAL.value:
                chat.id = member.id
                chat.title = f"{member.first_name} {member.last_name}"
                chat.chat_cover = member.profile_photo_url
            chat.latest_message_timestamp = self.format_timestamp(chat.latest_message_timestamp)

            chat_info = {
                'id': chat.id,
                'title': chat.title,
                'chat_cover': chat.chat_cover,
                'latest_message_timestamp': chat.latest_message_timestamp,
                'latest_message': chat.latest_message,
                'unread_messages': unread_messages_display
            }
            chat_data.append(chat_info)

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

        return render(request, 'enduser/chat/chats.html', {'chats': chat_data, 'follow': follow_data})

    def format_timestamp(self, timestamp):
        if not timestamp:
            return ''

        now = timezone.now()
        diff = now - timestamp
        if diff.days == 0:
            return timestamp.strftime('%H:%M')
        elif diff.days == 1:
            return 'Yesterday'
        elif diff.days < 7:
            return timestamp.strftime('%A')
        else:
            return timestamp.strftime('%d/%m/%Y')



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
    def get(self, request):    
        # user = request.user        
        user = user_service.get_user(2)
        title = "AbC"
        type = "2"
        members = [1, 2, 3]  # Example member IDs
        chat_cover = "exampleurl.com"
        chat_service.create_chat(title, members, chat_cover,user,type)                            
        return redirect('chat/')

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
        chat  = chat_service.chat_details(chat_id)
        title = "XYZ"
        members = [2, 4]
        chat_cover = "example.com"
        chat_service.update_chat(chat, title, members, chat_cover)        
        return redirect('chat/')
    
class ChatDeleteView(View):
    def post(self, request, chat_id):
        chat = chat_service.get_chat(chat_id)
        chat_service.delete_chat(chat)
        return redirect('chat_list')
class chatListViewApi(View):
    def get(self, request):
        user = user_service.get_user(2)
        chats =chat_service.list_chats_api(request,user)
        return JsonResponse(list(chats), safe=False)
class followerViewApi(View):
    def get(self, request):
        user = user_service.get_user(2)
        followers =chat_service.list_followers_api(request,user)
        return JsonResponse(list(followers), safe=False)

    