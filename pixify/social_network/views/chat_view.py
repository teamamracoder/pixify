from django.views import View
from ..services import chat_service, message_service, user_service
from django.shortcuts import render, redirect

class ChatListView(View):
    def get(self, request):
        chats = chat_service.list_chats()
        return render(request, 'enduser/chat/chats.html',{'chats':chats})

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

class ChatDetailsView(View):
    def get(self, request, chat_id):
        chat = chat_service.chat_details(chat_id)
        messages = message_service.list_messages_by_chat_id(chat_id)
        return render(request, 'enduser/chat/messages.html',{'chat':chat,'messages':messages})    
    
class ChatUpdatesView(View):
    def get(self, request, chat_id):
        # database data jabe
        chat  = chat_service.chat_details(chat_id)
        title = "XYZ"
        members = [2, 4]
        chat_cover = "example.com"
        chat_service.update_chat(chat, title, members, chat_cover)        
        return redirect('chat/')
    
class ChatDeleteView(View):
    def get(self, request, chat_id):
        chat_service.delete_chat(chat_id)
        return render(request, 'enduser/chat/chats.html')   
        
