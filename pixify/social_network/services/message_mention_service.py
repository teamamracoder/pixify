from ..models import ChatMember
from django.db.models import Q

def create_message_mentions(message,user):
    MessageMention.objects.create(message=message,user=user)
    
def list_messages_mention_Api(chat, user, search_query):
    if search_query:
        mention = ChatMember.objects.filter(chat_id=chat).filter(
            Q(member_id__first_name__icontains=search_query) | Q(member_id__last_name__icontains=search_query)
        ).values(
            'member_id', 'member_id__first_name', 'member_id__last_name', 'member_id__profile_photo_url'
        )
    else:
        mention = ChatMember.objects.filter(chat_id=chat).exclude(member_id=user).values(
            'member_id', 'member_id__first_name', 'member_id__last_name', 'member_id__profile_photo_url'
        )
    
    mention_list = list(mention)
    mention_list.insert(0, {'member_id': 'all', 'member_id__first_name': 'All', 'member_id__last_name': '', 'member_id__profile_photo_url': 'all-photo'})      
    return mention_list
