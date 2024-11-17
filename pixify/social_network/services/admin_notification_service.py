from .. import models
from django.shortcuts import get_object_or_404
from django.db.models import Q 

# def list_notifications():
#     return models.Notification.objects.all()
def get_notification(notification_id):
    return get_object_or_404(models.Notification, id=notification_id)


def admin_list_notifications(sort_by='text'):
    return models.Notification.objects.all().order_by(sort_by)

def admin_create_notification(**kwargs):
    notification = models.Notification.objects.create(
            receiver_id=kwargs['receiver_id'],
            text=kwargs['text'],           
            media_url=kwargs.get('media_url'),
            is_read=kwargs['is_read'],  
            is_active=kwargs.get('is_active', True), 
            created_by=kwargs['created_by'] 
        )
    return notification

def admin_update_notifications(**kwargs):
    notification = models.Notification.objects.create(
            id= kwargs['id'],
            receiver_id=kwargs['receiver_id'],
            text=kwargs['text'],           
            media_url=kwargs.get('media_url'),
            is_read=kwargs['is_read']
            
        )
    return notification



# def delete_notifications(notification):
#     notification.delete()


def admin_list_notifications_filtered(search_query, sort_by='text'):
    if search_query:
        # Use Q objects to filter by first_name, last_name, or email
        return models.Notification.objects.filter(
            Q(text__icontains=search_query) | 
            Q(media_url__icontains=search_query) |
            Q(is_read__icontains=search_query)
        ).order_by(sort_by)
    return models.Notification.objects.all().order_by(sort_by)
