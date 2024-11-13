from django.shortcuts import render, redirect
from django.views import View
from ..models import Message,User
from ..services import chat_service, message_service,user_service
from ..constants import ChatType

class ChatListView(View):
    def get(self, request):
        chats = chat_service.list_chats()
        user= user_service.get_user(1)
        chat_data = []
        for chat in chats:
            if chat.type ==ChatType.GROUP.value :
                chat_info = {
                    'title': chat.title,  
                    'photo': chat.chat_cover,   
                }  
            elif chat.type ==ChatType.PERSONAL.value:
                chat_info= {
                    'photo': user.profile_photo_url,
                    'title': user.first_name
                } 
            last_message = Message.objects.filter(chat_id=chat.id).order_by('-send_at').first()
            last_message_time = Message.objects.filter(chat_id=chat.id).order_by('-send_at').values('send_at').first()
            chat_info['last_message'] = last_message
            chat_info['last_message_time'] = last_message_time
            unread_count = self.get_unread_message_count(user.id, chat.id)
            chat_info['unread_count'] = unread_count
            print(unread_count)
            chat_data.append(chat_info)
        return render(request, 'enduser/chat/chats.html', {'chats': chat_data})
    def get_unread_message_count(self,user_id, chat_id):
        unread_count = Message.objects.filter(
            chat_id=chat_id,
            is_active=True
        ).exclude(sender_id=user_id).count()  
        return unread_count
    

class ChatCreateView(View):
    def post(self, request, user_id): 
        data = chat_service.get_user_data(user_id)
        print(data)
        return render(request, '#.html', {
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