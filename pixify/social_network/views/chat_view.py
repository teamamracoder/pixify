from django.shortcuts import render,redirect
from django.views import View
from ..services import chat_service, user_service,message_service, chat_member_service
from django.http import JsonResponse
from ..constants import ChatType
from ..models import User
from django.utils import timezone

class ChatListView(View):
    def get(self, request):
        user = request.user 
        chats = chat_service.list_chats_by_user(user)
        followers, followings = chat_service.get_all_user_follow(user)
        chat_data = []
        if not chats:
            no_chat_message="No chats available"
            return render(request, 'enduser/chat/chats.html',no_chat_message)
        for chat in chats:
            member = chat_service.count_members(chat.id)
            if member.count() < 2:
                continue
            unread_messages = message_service.unread_count(chat, user)
            unread_messages_display = '' if unread_messages == 0 else '10+' if unread_messages > 10 else str(unread_messages)

            if not chat.latest_message:
                chat.latest_message = ''

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
                
            latest_message_timestamp = self.format_timestamp(chat.latest_message_timestamp)
            chat_info = {
                'id': chat.id,
                'title': title,
                'chat_cover': chat_cover,
                'latest_message_timestamp': latest_message_timestamp,
                'latest_message': chat.latest_message,
                'unread_messages': unread_messages_display,
                'is_group' :chat.type==ChatType.GROUP.value
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
            return timestamp.strftime('%I:%M %p')
        elif diff.days == 1:
            return 'Yesterday'
        elif diff.days < 7:
            return timestamp.strftime('%A')
        else:
            return timestamp.strftime('%d/%m/%Y')


class ChatCreateView(View):
    def get(self, request):
        user = user_service.get_user(request)
        return render(request, 'enduser/chat/chats.html',{'user':user})         

    def post(self,request):                
        user=request.POST['user']        
        type = request.POST['type']
        members = request.POST.getlist('members')        

        if type == ChatType.PERSONAL.value:            
            title = None
            chat_cover = None

        elif type == ChatType.GROUP.value:    
            title = request.POST['titel','']                    
            chat_cover = request.POST.get('chat_cover', '')
    
        chat=chat_service.create_chat(user,title, chat_cover,type)           
        members.append(user.id) 
        for member in members:   
            chat_member_service.create_chat_member(chat,member,user)
        return redirect('chat/')         


class ChatDetailsView(View):
    def get(self, request, chat_id):
        user = request.user 
        chat = chat_service.get_chat_by_id(chat_id)
        messages = message_service.list_messages_by_chat_id(chat_id)
        # chat_data=[]
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
            'is_group' :chat.type==ChatType.GROUP.value
        }
        # chat_data.append(chat_info)       
        return render(request, 'enduser/chat/messages.html',{'chat':chat_info,'messages':messages,'user':user})
    
class ChatUpdateView(View):   
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
    def post(self, request, chat_id):
        chat = chat_service.get_chat_by_id(chat_id)
        chat_service.delete_chat(chat)
        return redirect('chat_list')

class ChatListViewApi(View):
    def get(self, request):
        user = request.user
        chats = chat_service.list_chats_by_user(user)
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
                chat_cover = chat.chat_cover or '\static\images\group_pic.png'
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
                        'chat_cover':'\static\images\group_pic.png',
                    } 
            chat_data_list.append(chat_info)
        chats = chat_service.list_chats_api(request,chat_data_list)
        return JsonResponse(chats, safe=False)

    

