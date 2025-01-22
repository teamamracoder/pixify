from .. import models
from django.shortcuts import get_object_or_404
from django.db.models import Q 


def manage_get_notification(notification_id):
    return get_object_or_404(models.Notification, id=notification_id)


def manage_create_notification(**kwargs):
    notification = models.Notification.objects.create(
            receiver_id=kwargs['receiver_id'],
            text=kwargs['text'],           
            media_url=kwargs.get('media_url'),
            is_read=kwargs['is_read'],  
            is_active=kwargs.get('is_active', True), 
            created_by=kwargs['created_by'] 
        )
    return notification

def manage_update_notification(notification, text,receiver_id,media_url, is_read):
    notification.text = text
    notification.receiver_id = receiver_id
    notification.media_url = media_url
    notification.is_read = is_read     
    notification.save()
    return notification

from django.db.models import Q
from . import models

def manage_list_notifications_filtered(search_query=None, sort_by='text'):
    if search_query:
        # Use Q objects to filter by text, media_url, or is_read
        return models.Notification.objects.filter(
            Q(text__icontains=search_query) | 
            Q(media_url__icontains=search_query) |
            Q(is_read__icontains=search_query)
        ).order_by(sort_by)
    return models.Notification.objects.all().order_by(sort_by)

def unread_notifications_count(user_id):
    """
    Count the number of unread notifications for a specific user.
    """
    return models.Notification.objects.filter(receiver_id=user_id, is_read=False, is_active=True).count()



