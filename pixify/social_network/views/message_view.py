from django.shortcuts import render, redirect ,get_object_or_404
from django.views import View
from ..services import message_reaction_service,user_service,message_service,send_reply_service

class messageView(View):
    def get(self, request):
        return render(request, 'enduser/message/index.html')

class MessageReactionCreateView(View):
    def get(self, request):
        reacted_by= user_service.get_user(1)
        message_id= message_service.get_message(2)
        reaction_type='abcd'
        message_reaction_service.create_message_reaction(reacted_by,message_id,reaction_type)
        
class MessageReactionUpdateView(View):
    def get(self, request, message_reaction_id):
        message_reaction =message_reaction_service.get_message_reaction(message_reaction_id)
        reacted_by = user_service.get_user(1)
        message_id = message_service.get_message(2)
        reaction_type ='avc' 
        message_reaction_service.update_message_reaction(reacted_by, message_id, reaction_type)

class  MessageReactionDeleteView(View): 
    def get(self, request, message_reaction_id):
        message_reaction = message_reaction_service.get_message_reaction(message_reaction_id)

class  send_reply(View):
    def get(self,request,message_id):
        text= text
        media_url= media_url
        sender_id= sender_id
        chat_id= chat_id
        reply_for_message_id=reply_for_message_id
        send_at=send_at
        reply_for_every_everyone=reply_for_every_everyone
        mentions=mentions
    

    