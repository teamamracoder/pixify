from ..models import ChatMember,User
from ..services import chat_service, user_service

def add_chat_member(chat_id, user_id, auth_user): 
    user = user_service.get_user(user_id)
    chat = chat_service.get_chat_by_id(chat_id)

    chat_member, created = ChatMember.objects.get_or_create(
        chat_id=chat,
        member_id=user,
        defaults={
            'created_by': auth_user,
            'updated_by': auth_user,
            'is_active': True
        }
    )

    if not created:  # The member already exists
        chat_member.is_active = True  # Or other fields if needed
        chat_member.updated_by = auth_user
        chat_member.save()

    
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

