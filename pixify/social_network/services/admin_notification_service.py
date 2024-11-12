from .. import models
from django.shortcuts import get_object_or_404

def list_notifications():
    return models.Notification.objects.all()

def create_notifications(text, media_url, receiver_id,is_read ):
    return models.Notification.objects.create(text=text, media_url=media_url, receiver_id=receiver_id,is_read=is_read)

def delete_notifications(notification):
    notification.delete()
