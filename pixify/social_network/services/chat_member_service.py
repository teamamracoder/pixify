from ..models import Chat, User, ChatMember

def add_member_to_chat(chat_id, user_id):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        ChatMember.objects.create(chat_id=chat, member_id=user)
    
    
def remove_member_from_chat(chat_id, user_id):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        ChatMember.objects.filter(chat_id=chat, member_id=user).delete()
