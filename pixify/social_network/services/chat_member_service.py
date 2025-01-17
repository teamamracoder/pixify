from ..models import ChatMember,User
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

def get_chat_members(chat_id):
    # Get all the ChatMember instances for the given chat_id
    chat_members = ChatMember.objects.filter(chat_id=chat_id, is_active=True)
    # Extract only the ids of the related User objects
    user_ids = chat_members.values_list('member_id', flat=True)
    return user_ids

