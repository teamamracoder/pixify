from django.shortcuts import render, redirect
from django.views import View
from .. import services

# everyone insert data manually
# user (5)
# chats (4)--> perasonal chat(2)
#           --> group chat(2)
# messages (each chats, 3 message)-->use different sender_id
# message read status (as required, initially blank)
class ChatView(View):
    def get(self, request):

    #    get all chats for the logged in user
    #      loop over the chats
    #           
        #     # chat type
        #     # if chattype personal
        #         # chat->member(who is not the loggedinuser)->fullname 
        #         # chat->member(who is not the loggedinuser)->photo
        #     #if group
        #         #chat->title
        #         #chat->coverphoto
        #     # message->findby_chat_id->all->id(desc)->first
        #     #                                       ->created_at
        #     #                                        ->msg
    
    #   users = [all follower/following without self]  but follwer/following of the logged user
    #     data = {
    #         'title'=>'fetch',
    #         'photo'=>'fetch',
    #         'last_message'=>'fetch',
    #         'last_message_time'=>'fetch',
    #         'unread_count'=>'fetch',
    #          'users'=>users
    #     }
        return render(request, 'enduser/message/index.html')
    
    def createChat():
        return
        # loggin = 3
        
        # memebers (2,4,3)
        # dinal members =set(2,4,3,3)
        
        # as memebers=single,  then, type=pesonal
        # chats(memeber), 2,1 and type=pesonal   
        # if chat available do not create new chat, redirect to that chatbox
        # else create new chat, redirect to their chatbox
        
        # mmebers 1,3
        # as memebers=multiple, then type=group
        # create new group 

class ChatAdminListView(View):
    def get(self, request):
        chats = services.chat_service.list_chats()
        return render(request, 'adminuser/chat/list.html',{'chats':chats})


class ChatAdminCreateView(View):
    def get(self, request):       
        return render(request, 'adminuser/chat/create.html')

    def post(self, request):
        title=request.POST['title']
        # member=request.POST['member']
        type=request.POST['type']
        is_active=request.POST.get('is_active' 'True')=='True'
        created_at=request.POST.getlist('created_at')
        updated_at=request.POST.getlist('updated_at')
        created_by_id=request.POST.getlist('created_by_id')
        updated_by_id=request.POST.getlist('updated_by_id')
        chat_cover=request.POST.getlist('chat_cover')
        services.chat_service.create_chats(title,type,is_active,created_at,updated_at,created_by_id,updated_by_id,chat_cover)
        return redirect ('chat_list')
    
class ChatAdminDetailView(View):
    def get(self, request, chat_id):
        chat = services.chat_service.get_chat(chat_id)
        return render(request, 'adminuser/chat/detail.html', {'chat': chat}) 
        

class ChatAdminUpdateView(View):
    def get(self, request,chat_id):
        chat = services.chat_service.get_chat(chat_id)
        return render(request, 'adminuser/chat/update.html',{'chat': chat})

    def post(self, request, chat_id):
        chat = services.chat_service.get_chat(chat_id)
        title = request.POST['title']
        type = request.POST['type']
        
        services.chat_service.update_chats(chat, title,type)
        return redirect('chat_detail', chat_id=chat.id)
    

class ChatAdminDeleteView(View):
    def get(self, request, chat_id):
        chat = services.chat_service.get_chat(chat_id)
        return render(request, 'adminuser/chat/delete.html',{'chat': chat})

    def post(self, request, chat_id):
        chat= services.chat_service.get_chat(chat_id)
        services.chat_service.delete_chats(chat)
        return redirect('chat_list')
