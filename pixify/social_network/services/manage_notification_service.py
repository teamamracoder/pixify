from ..models import Notification
from ..packages.get_data import GetData
from .. import models
from django.shortcuts import get_object_or_404
from django.db.models import Q 


def manage_list_notifications():
    return Notification.objects.all()


def manage_get_notification(notification_id):
    return get_object_or_404(models.Notification, id=notification_id)


def manage_create_notification(**kwargs):
    notification = models.Notification.objects.create(
            receiver_id=kwargs['receiver_id'],
            text=kwargs['text'],           
            media_url=kwargs.get('media_url'),
            # is_read=kwargs['is_read'],  
            # is_active=kwargs.get('is_active', True), 
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


def manage_list_notifications_filtered(search_query, sorting_order, sort_by, page_number):
    # get data
    data = (
        GetData(Notification)
        .search(search_query,"text","media_url", "is_read")
        .sort(sort_by, sorting_order)
        .paginate(limit=3, page=page_number)
        .execute()
    )
    # return data
    return data