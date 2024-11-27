from ..models import ChatMember,MessageMention
from django.db.models import Q
 
def create_message_mentions(message,user,auth_user):
    MessageMention.objects.create(message=message,user=user,created_by=auth_user)

def delete_message_mentions(message,user):
    mentions = MessageMention.objects.filter(message=message)
    for mention in mentions:
        mention.is_active = False
        mention.updated_by=user
        mention.save()

def list_messages_mention_Api(chat, user, search_query, exclude_ids, mentioned_all):
    if search_query:
        mention = ChatMember.objects.filter(chat_id=chat).exclude(member_id__in=exclude_ids).exclude(member_id=user).filter(
            Q(member_id__first_name__icontains=search_query) | Q(member_id__last_name__icontains=search_query)
        ).values(
            'member_id', 'member_id__first_name', 'member_id__last_name', 'member_id__profile_photo_url'
        )
        print(f"Filtered mentions with search query '{search_query}': {mention}")
    else:
        mention = ChatMember.objects.filter(chat_id=chat).exclude(member_id=user).exclude(member_id__in=exclude_ids).values(
            'member_id', 'member_id__first_name', 'member_id__last_name', 'member_id__profile_photo_url'
        )
        print("Mentions without search query:", mention)

    mention_list = list(mention)
    if not mentioned_all:
        mention_list.insert(0, {'member_id': 'all', 'member_id__first_name': 'All', 'member_id__last_name': '', 'member_id__profile_photo_url': 'all-photo'})
    return mention_list