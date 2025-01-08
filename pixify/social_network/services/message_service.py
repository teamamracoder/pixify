from ..models import Message,MessageReadStatus
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta


def list_messages_by_chat_id(chat_id,user_id):  
    messages = Message.objects.filter(chat_id=chat_id, is_active=True)
    for message in messages:
        if not MessageReadStatus.objects.filter(message_id=message, read_by_id=user_id).exists():
            MessageReadStatus.objects.create(
                message_id=message,
                read_by_id=user_id,
                read_at=timezone.now(),
                created_by_id=user_id) 
    return messages

def create_message(text, media_url,sender_id, chat):
    return Message.objects.create(
        text=text,
        media_url=media_url,
        sender_id=sender_id,
        chat_id=chat,
        created_by=sender_id
    )

def get_message_by_id(message_id):
    return get_object_or_404(Message, id=message_id,is_active=True)

def update_message(message, text, media_url,user):
    message.text = text
    message.media_url = media_url
    message.updated_by=user
    message.save()
    return message

def delete_message(message,user):
        message.is_active=False
        message.updated_by=user
        message.save()

def reply_message(user, text, media_urls, sender_id, chat_id, reply_for_message):
    return Message.objects.create(
        text=text,
        media_url=media_urls,
        sender_id=sender_id,
        chat_id=chat_id,
        reply_for_message_id=reply_for_message,
        created_by=user
    )
 
def unread_count(chat,user):    
    unread_count = Message.objects.filter(
        chat_id=chat,
        is_active=True
        ).exclude(
        fk_message_msg_status_messages_id__read_by=user
    ).count()  
    return unread_count

def is_editable(message):
        # Check if the message can be edited within 10 minutes of creation.
        time_difference = timezone.now() - message.created_at
        return time_difference <= timedelta(minutes=10)

 # Apply timestamp formatting
def format_timestamp(timestamp):
    if not timestamp:
        return ''
    now = timezone.now()
    # Normalize both timestamps to the start of their respective days
    now_date = now.date()
    timestamp_date = timestamp.date()
    diff = now_date - timestamp_date
    if diff.days == 0:
        return 'Today'
    elif diff.days == 1:
        return 'Yesterday'
    elif diff.days < 7:
        return timestamp.strftime('%A')  # Day name
    else:
        return timestamp.strftime('%d/%m/%Y')  # Full date

# Custom function to define sorting order
def sort_key(item):
    formatted_timestamp, messages = item
    now = timezone.now()

    if formatted_timestamp == 'Today':
        # Return today's date as the highest priority
        return [now]
    elif formatted_timestamp == 'Yesterday':
        # Return yesterday's date
        return [now - timedelta(days=1)]
    elif formatted_timestamp in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        # Map weekdays to dates within the past week
        current_weekday = now.weekday()
        weekday_to_index = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6,
        }
        target_weekday = weekday_to_index[formatted_timestamp]
        # Calculate the date difference for the target day in the past week
        days_difference = (current_weekday - target_weekday) % 7
        target_date = now - timedelta(days=days_difference)
        return [target_date]
    else:
        # Parse specific dates and make them timezone-aware
        specific_date = datetime.strptime(formatted_timestamp, '%d/%m/%Y')
        specific_date_aware = timezone.make_aware(specific_date, timezone.get_current_timezone())
        return [specific_date_aware]
    

def is_editable(message):
        # Check if the message can be edited within 10 minutes of creation.
        time_difference = timezone.now() - message.created_at
        return time_difference <= timedelta(minutes=10)

 # Apply timestamp formatting
def format_timestamp(timestamp):
    if not timestamp:
        return ''
    now = timezone.now()
    # Normalize both timestamps to the start of their respective days
    now_date = now.date()
    timestamp_date = timestamp.date()
    diff = now_date - timestamp_date
    if diff.days == 0:
        return 'Today'
    elif diff.days == 1:
        return 'Yesterday'
    elif diff.days < 7:
        return timestamp.strftime('%A')  # Day name
    else:
        return timestamp.strftime('%d/%m/%Y')  # Full date

# Custom function to define sorting order
def sort_key(item):
    formatted_timestamp, messages = item
    now = timezone.now()

    if formatted_timestamp == 'Today':
        # Return today's date as the highest priority
        return [now]
    elif formatted_timestamp == 'Yesterday':
        # Return yesterday's date
        return [now - timedelta(days=1)]
    elif formatted_timestamp in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        # Map weekdays to dates within the past week
        current_weekday = now.weekday()
        weekday_to_index = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6,
        }
        target_weekday = weekday_to_index[formatted_timestamp]
        # Calculate the date difference for the target day in the past week
        days_difference = (current_weekday - target_weekday) % 7
        target_date = now - timedelta(days=days_difference)
        return [target_date]
    else:
        # Parse specific dates and make them timezone-aware
        specific_date = datetime.strptime(formatted_timestamp, '%d/%m/%Y')
        specific_date_aware = timezone.make_aware(specific_date, timezone.get_current_timezone())
        return [specific_date_aware]

def get_latest_message(chat_id):
    return Message.objects.filter(chat_id=chat_id, is_active=True).order_by('-send_at').first()