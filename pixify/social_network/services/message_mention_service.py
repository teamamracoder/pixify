from ..models import ChatMember,MessageMention,User
from django.db.models import Q
from social_network.utils.common_utils import print_log 
 
def create_message_mentions(message,user,auth_user):
    MessageMention.objects.create(message=message,user=user,created_by=auth_user)

def delete_message_mentions(message,user):
    mentions = MessageMention.objects.filter(message=message)
    for mention in mentions:
        mention.is_active = False
        mention.updated_by=user
        mention.save()


def list_messages_mention_Api(chat, user, search_query, exclude_ids, mentioned_all):
    print_log(f"Search Query: {search_query}, Exclude IDs: {exclude_ids}, Mentioned All: {mentioned_all}")
    
    numeric_ids = [id for id in exclude_ids if id.isdigit()]
    string_mentions = [id for id in exclude_ids if not id.isdigit()]
        
    user_ids_to_exclude = numeric_ids[:]

    for username in string_mentions:
        if username != 'all': 
            # mentioned_all=not(mentioned_all)
    
            user_obj = User.objects.filter(first_name=username).first()
            if user_obj:
                user_ids_to_exclude.append(str(user_obj.id))
    print_log(mentioned_all)
    print_log(f"Resolved Exclusion IDs: {user_ids_to_exclude}")
    
    mention = ChatMember.objects.filter(chat_id=chat).exclude(member_id=user)
    
    if user_ids_to_exclude:
        mention = mention.exclude(member_id__in=user_ids_to_exclude)
    
    if search_query:
        mention = mention.filter(Q(member_id__first_name__icontains=search_query) |Q(member_id__last_name__icontains=search_query))
    
    mention_list = list(mention.values('member_id','member_id__first_name','member_id__last_name','member_id__profile_photo_url'))
    
    if not mentioned_all:
        mention_list.insert(0, {"member_id": "all","member_id__first_name": "All","member_id__last_name": "","member_id__profile_photo_url": "/path/to/all/icon.png"})

    print_log(f"Mention List: {mention_list}")
    return mention_list
