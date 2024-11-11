from django.views import View
from ..services import chat_service, message_service
from django.shortcuts import render

class ChatListView(View):
    def get(self, request):
        chats = chat_service.list_chats()
        return render(request, 'enduser/chat/chats.html',{'chats':chats})

class ChatCreateView(View):
    def get():
        # database data asbe
        return
    
    def post():
        # database data jabe
        return
    
class ChatDetailsView(View):
    def get(self, request, chat_id):
        chat = chat_service.chat_details(chat_id)
        messages = message_service.list_messages_by_chat_id(chat_id)
        return render(request, 'enduser/chat/messages.html',{'chat':chat,'messages':messages})
    
class ChatUpdatesView(View):
    def get():
        # database data asbe
        return
    
    def post():
        # database data jabe
        return
    
class ChatDeleteView(View):
    def get():
        return