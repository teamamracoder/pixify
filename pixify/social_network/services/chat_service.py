from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404

def list_chats():
    return Chat.objects.all()

def chat_details(chat_id):
    return get_object_or_404(Chat, id=chat_id)


def create_chat(title, members, chat_cover, user,type):
            
    chat = Chat.objects.create(title=title, members=members, chat_cover=chat_cover, created_by=user,type=type)        

    for member_id in members:
        member = User.objects.get(id=member_id)
        ChatMember.objects.create(chat_id=chat, member_id=member, created_by=user)
    return chat

def update_chat(chat, title, members, chat_cover):    
        chat.title = title  
        chat.chat_cover = chat_cover                
        chat.members.clear()                
        for member_id in members:
            member = User.objects.get(id=member_id)
            ChatMember.objects.create(chat_id=chat, member_id=member)                
        chat.save()
        return chat    

def delete_chat(chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.is_active = False
    chat.save()


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