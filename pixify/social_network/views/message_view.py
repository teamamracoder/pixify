from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..services import message_service

class messageView(View):
    def get(self, request):
        return render(request, 'enduser/message/index.html')  

class messageCreateView(View):
    def get(self, request):        
        text = "hi"
        media_url = "null"
        sender_id = 1 
        chat_id = 2  

        message_service.create_message(text, media_url, sender_id, chat_id)
        return render(request, 'enduser/message/index.html')

class messageUpdateView(View):
    def get(self, request, message_id):
        message = message_service.get_message(message_id)        
        text = "hello"
        media_url = "null"
        message_service.update_message(message, text, media_url)
        return render(request, 'enduser/message/index.html')

class messageDeleteView(View):
    def get(self, request, message_id):
        message_service.delete_message(message_id)
        return render(request, 'enduser/message/index.html')