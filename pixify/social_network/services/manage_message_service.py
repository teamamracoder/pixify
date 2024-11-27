from ..models import Message
from ..packages.get_data import GetData
from ..import models
from django.shortcuts import get_object_or_404

# def get_messages():
#     return Message.objects.all()

#get messages
def manage_get_message(message_id):
    return get_object_or_404(models.Message, id=message_id)

def manage_create_message(**kwargs):
    message = models.Message.objects.create(      
            text=kwargs['text'],           
            media_url=kwargs.get('media_url'),  
            chat_id=kwargs['chat_id'],
            created_by=kwargs['created_by'] ,
            sender_id=kwargs['sender_id'] 
        )
    return message

def manage_list_messages_filtered(search_query, sort_by,  sorting_order, page_number):
    # get data
    data = (
        GetData(Message)
        .search(search_query,"text","media_url")
        .sort(sort_by, sorting_order)
        .paginate(limit=10, page=page_number)
        .execute()
    )
    # return data
    return data

