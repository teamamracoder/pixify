from ..models import Chat
from django.shortcuts import get_object_or_404

def list_chats():
    return Chat.objects.all()

def chat_details(chat_id):
    return get_object_or_404(Chat, id=chat_id)






# from .. import models
# from django.shortcuts import get_object_or_404

# def list_chat():
#     return models.Chat.objects.all()

# def create_chat(reciver,sender):
#     return models.Chat.objects.create(reciver=reciver,sender=sender)

# def get_chat_(chat_id):
#     return get_object_or_404(models.Chat, id=chat_id)

# def get_chat_messages(chat_room):
#     return models.Message.objects.filter(chat_room=chat_room).order_by('timestamp')

# def create_message(chat_room, user, content):
#     return models.objects.create(room=chat_room, user=user, content=content)

# def delete_chat(chat_room):
#     chat_room.delete()