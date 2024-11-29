from ..models import ChatMember
from ..services import chat_service, user_service

def create_chat_member(chat_id, user_id, auth_user): 
        user = user_service.get_user(user_id)
        chat = chat_service.get_chat_by_id(chat_id)
        ChatMember.objects.create(chat_id=chat, member_id=user, created_by=auth_user,updated_by=auth_user)
    
def delete_chat_member(chat_id, user_id, auth_user): 
        user = user_service.get_user(user_id)
        chat = chat_service.get_chat_by_id(chat_id)
        chat_member = ChatMember.objects.get(chat_id=chat, member_id=user)
        chat_member.updated_by = auth_user
        chat_member.is_active=False
        chat_member.save()