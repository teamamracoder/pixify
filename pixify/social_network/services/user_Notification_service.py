from .. import models
from django.shortcuts import get_object_or_404
from django.db.models import Q 


from social_network.models.notification_model import Notification 

def count_notification():
    return Notification.objects.all()


def count_unread_notifications(user_id):
    return Notification.objects.filter(receiver_id=user_id, is_read=False).count() 


from datetime import datetime, timedelta
from django.utils.timezone import now

def time_ago(time):
    diff = now() - time
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    
    minutes = seconds // 60
    if minutes < 60:
        return f"{int(minutes)}m"
    
    hours = minutes // 60
    if hours < 24:
        return f"{int(hours)}h"
    
    days = hours // 24
    if days < 7:
        return f"{int(days)}d"
    
  
    return time.strftime('%b %d, %Y')

