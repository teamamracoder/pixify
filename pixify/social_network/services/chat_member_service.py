from ..models import Chat, User, ChatMember

def create_chat_member(chat_id, user_id, auth_user):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        ChatMember.objects.create(chat_id=chat, member_id=user, created_by=auth_user)
    
    
def delete_chat_member(chat_id, user_id, auth_user):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        # ChatMember.objects.filter(chat_id=chat, member_id=user).delete()
        # data should be is_active
        # as we are updating, pass auth_user to updated_by
