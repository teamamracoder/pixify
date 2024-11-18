from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..services import message_service,user_service, message_reaction_service

class MessageReactionCreateView(View):
    def post(self, request):
        reacted_by= user_service.get_user(1)
        message_id= message_service.get_message_by_id(2)
        reaction_type='abcd'
        message_reaction_service.create_message_reaction(reacted_by,message_id,reaction_type)
        
class MessageReactionUpdateView(View):
    def post(self, request, message_reaction_id):
        message_reaction =message_reaction_service.get_message_reaction_by_id(message_reaction_id)
        reacted_by = user_service.get_user(1)
        message_id = message_service.get_message_by_id(2)
        reaction_type ='avc' 
        message_reaction_service.update_message_reaction(reacted_by, message_id, reaction_type)

class  MessageReactionDeleteView(View): 
    def post(self, request, message_reaction_id):
        message_reaction = message_reaction_service.get_message_reaction_by_id(message_reaction_id)