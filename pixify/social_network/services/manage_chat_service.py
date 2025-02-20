from ..packages.get_data import GetData
from ..models import Chat, User, ChatMember
from django.shortcuts import get_object_or_404
from django.db.models import Q



def manage_list_chats(sort_by='title'):
  return Chat.objects.all().order_by(sort_by)

def manage_create_chats(title,type,created_by,chat_cover):
  return Chat.objects.create(title=title,type=type,created_by=created_by,chat_cover=chat_cover)


def manage_get_member(chat_id):
    chat_members = ChatMember.objects.filter(chat_id=chat_id)
    member_ids = [member.member_id_id for member in chat_members]
    chat_members = User.objects.filter(id__in=member_ids)  # Get all users with IDs in member_ids
    print(chat_members)
    return chat_members

# def manage_get_member(chat_id):
#     # First, get all members for the specific chat_id
#    chat_members = ChatMember.objects.filter(chat_id=chat_id)

#    # Initialize a list to store member details
#    members_info = []

#    # Loop through each chat member and get the associated user information
#    for chat_member in chat_members:
#       member_id = chat_member.member_id  # The member_id is the foreign key to the User table
#       user_id = member_id.id
#       # Get the user details for the member_id
#       try:
#             user = User.objects.get(id=user_id)  # Fetch user by member_id

#             # Add user information to the members_info list
#             members_info.append({
#                'id': user.id,
#                'username': user.username,  # You can add other fields from the User model as needed
#                'email': user.email,
#                'first_name': user.first_name,
#                'last_name': user.last_name,
#             })
#       except User.DoesNotExist:
#             # Handle the case where the user doesn't exist
#             members_info.append({
#                'id': member_id,
#                'username': 'Unknown',  # You can handle this case as you see fit
#                'email': 'Unknown',
#                'first_name': 'Unknown',
#                'last_name': 'Unknown',
#             })

#    return members_info

def get_chat_member_by_member_id(chat_member):
#    user_chat_member= User.objects.filter(id=chat_member, is_active=True)
   user_chat_member= User.objects.all()
   return user_chat_member

def manage_get_chat(chat_id):
   return get_object_or_404 (Chat , id=chat_id)


def manage_update_chats(chat,title,type,chat_cover, updated_by):
   chat.title=title
   chat.type=type

#    chat.created_by=created_by
   chat.chat_cover=chat_cover
   chat.updated_by=updated_by

   chat.save()
   return chat

def manage_delete_chats(chat):
    chat.delete()

def manage_list_chats_filtered(search_query, sorting_order, sort_by, page_number):

    # get data
    data = (
        GetData(Chat)
        .search(search_query,"title","type","chat_cover")
        .sort(sort_by, sorting_order)
        .paginate(limit=10, page=page_number)
        .execute()
    )
    # return data
    return data

