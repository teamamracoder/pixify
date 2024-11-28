from .. import models
from django.shortcuts import get_object_or_404
from django.db.models import Q 


from social_network.models.notification_model import Notification 

def count_notification():
    return Notification.objects.all()

from datetime import datetime, timedelta
from django.utils.timezone import now

def time_ago(time):
    diff = now() - time
    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if seconds < 60:
        return "just now"
    elif minutes < 60:
        return f"{int(minutes)}m"
    elif hours < 24:
        return f"{int(hours)}h"
    elif days < 7:
        return f"{int(days)}d"
    else:
        return time.strftime('%b %d, %Y')
