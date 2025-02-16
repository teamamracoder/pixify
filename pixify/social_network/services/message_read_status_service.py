from ..models import MessageReadStatus

def create_message_read_status(message_id, user):
    MessageReadStatus.objects.get_or_create(    
        message_id=message_id,
        read_by=user,
        created_by=user,
        updated_by=user
    )
    
       