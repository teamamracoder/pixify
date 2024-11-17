from django.shortcuts import render,redirect
from django.views import View
from django.utils import timezone
from django.utils.timezone import localtime
from ..models import Message, ChatMember, Follower
from ..services import chat_service, message_service, user_service
from ..constants import ChatType
from django.shortcuts import render,redirect
from .. import services

from ..models import User
from ..models import Chat
from ..constants import ChatType
from django.core.paginator import Paginator 
from django.http import HttpResponseBadRequest, JsonResponse


# everyone insert data manually
# user (5)
# chats (4)--> perasonal chat(2)
#           --> group chat(2)
# messages (each chats, 3 message)-->use different sender_id
# message read status (as required, initially blank)
class ChatView(View):
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
  

    def get(self, request):    
        # user = request.user        
        user = user_service.get_user(2)
        title = "AbC"
        type = "2"
        members = [1, 2, 3]  # Example member IDs
        chat_cover = "exampleurl.com"
        chat_service.create_chat(title, members, chat_cover,user,type)                            
        return redirect('chat/')

    def post():
        # database data jabe
        return
    
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


# Admin Section
#=============================================================================
class ChatAdminListView(View):
    def get(self, request):
        search_query = request.GET.get('search', '') 
        sort_by = request.GET.get('sort_by', 'title')
        sort_order = request.GET.get('sort_order', 'asc')
        page_number = request.GET.get('page', 1)


        # Adjust sort order for descending order
        if sort_order == 'desc':
            sort_by = '-' + sort_by

        # print(f"Search Query: {search_query}")
        # Get filtered and sorted users based on search
        chat = services.chat_service.list_chats_filtered(search_query, sort_by)

        # Paginate the users
        paginator = Paginator(chat, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)

        
        
        choices_type = [{type.value: type.name} for type in ChatType]

        return render(request, 'adminuser/chat/list.html', {
            'chats': page_obj,
            'choices_type': choices_type,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })



class ChatAdminCreateView(View):
    def get(self, request):       
        choices_type = [{type.value: type.name} for type in ChatType]
        return render(request, 'adminuser/chat/create.html',{"choices_type":choices_type})

    def post(self, request):
        chat_data={
        'title': request.POST['title'],      
        'type': request.POST['type'],       
        'chat_cover': request.POST.get('chat_cover', ''), 
        'is_active': request.POST.get('is_active', 'on') == 'on',
        'created_by': User.objects.get(id=request.POST['created_by'])
        # 'updated_by':User.objects.get(id=request.POST['updated_by'])
        }
        services.chat_service.create_chats(**chat_data)
        return redirect ('chat_list')
        
    
class ChatAdminDetailView(View):
    def get(self, request, chat_id):  
        choices_type = [{type.value: type.name} for type in ChatType]     
        chat = services.chat_service.get_chat(chat_id)
        return render(request, 'adminuser/chat/detail.html',{'chat':chat, "choices_type":choices_type }) 
        

class ChatAdminUpdateView(View):
    def get(self, request,chat_id):
        choices_type = [{type.value: type.name} for type in ChatType]
        chat = services.chat_service.get_chat(chat_id)
        return render(request, 'adminuser/chat/update.html',{'chat': chat, "choices_type":choices_type})

    def post(self, request, chat_id):
        chat = services.chat_service.get_chat(chat_id)
        chat_data={
            'updated_by': User.objects.get(id=request.POST['updated_by']),
            'title':request.POST.get('title'),
            'type':request.POST.get('type'),
            'chat_cover':request.POST.get('chat_cover'),
            'is_active':request.POST.get('is_active', 'on') == 'on',
            # 'created_by':request.POST.get('created_by'),
            # 'updated_by':request.POST.get('updated_by'),
        }

        required_fields = ['title', 'type', 'chat_cover']
        for field in required_fields:
            if not chat_data.get(field):
                return HttpResponseBadRequest(f"Missing required field: {field}")
        
        services.chat_service.update_chats(
            chat, **chat_data)
        return redirect('chat_detail', chat_id=chat.id)
    

class ChatAdminDeleteView(View):
    def get(self, request, chat_id):
        chat = chat_service.get_chat(chat_id)
        return render(request, 'adminuser/chat/delete.html',{'chat': chat})

    def post(self, request, chat_id):
        chat= chat_service.get_chat(chat_id)
        chat_service.delete_chats(chat)
        return redirect('chat_list')


class ToggleChatActiveView(View):
    def post(self, request, chat_id):
        chat = services.chat_service.get_chat(chat_id)
        chat.is_active = not chat.is_active  # Toggle active status
        chat.save()
        return JsonResponse({'is_active': chat.is_active})


class AdminToggleChatActiveView(View):
    def post(self, request, chat_id):
        chat = services.chat_service.get_chat(chat_id)
        chat.is_active = not chat.is_active  
        chat.save()
        return JsonResponse({'is_active': chat.is_active})