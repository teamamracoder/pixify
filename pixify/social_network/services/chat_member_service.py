from ..models import Chat, User, ChatMember

def create_chat_member(chat_id, user_id, auth_user):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        ChatMember.objects.create(chat_id=chat, member_id=user, created_by=auth_user,updated_by=auth_user)
    
    
def delete_chat_member(chat_id, user_id, auth_user):
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)        
        chat_member = ChatMember.objects.get(chat_id=chat, member_id=user) 
        chat_member.updated_by = auth_user         
        chat_member.is_active=False
        chat_member.save()
        
        # data should be is_active
        # as we are updating, pass auth_user to updated_by
