from .. import models
from django.shortcuts import get_object_or_404

def list_notifications():
    return models.Notification.objects.all()


def create_notifications(**kwargs):
    notification = models.Notification.objects.create(
            receiver_id=kwargs['receiver_id'],
            text=kwargs['text'],           
            media_url=kwargs.get('media_url'),
            is_read=kwargs['is_read'],  
            is_active=kwargs.get('is_active', True) 
            
        )
    return notification

def get_notification(notification_id):
    return get_object_or_404(models.Notification, id=notification_id)


def update_notifications(**kwargs):
    notification = models.Notification.objects.create(
            id= kwargs['id'],
            receiver_id=kwargs['receiver_id'],
            text=kwargs['text'],           
            media_url=kwargs.get('media_url'),
            is_read=kwargs['is_read']
            
        )
    return notification

# def update_notifications(notification, text,media_url,receiver_id, is_read):
#     notification.text = text
#     notification.media_url = media_url
#     notification.receiver_id = receiver_id
#     notification.is_read = is_read
#    
#     return notification

# def create_notifications(text, media_url, receiver_id,is_read ):
#     return models.Notification.objects.create(text=text, media_url=media_url, receiver_id=receiver_id,is_read=is_read)

# def delete_notifications(notification):
#     notification.delete()
