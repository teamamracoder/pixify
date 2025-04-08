from ..models import Notification   # Import the Notification model from the current package
from ..packages.get_data import GetData # Import GetData utility for handling database queries efficiently
from ..import models    # Import models module (used for referencing models dynamically)
from django.shortcuts import get_object_or_404  # Import Django's shortcut function to fetch objects or return a 404 error
from django.db.models import Q  # Import Q object for complex query filtering


# Function to retrieve all notifications
def manage_list_notifications():
    return Notification.objects.all()  # Fetch all notifications from the database

# Function to fetch a specific notification by ID
def manage_get_notification(notification_id):
    return get_object_or_404(models.Notification, id=notification_id)  # Returns notification or 404 error

# Function to create a new notification entry in the database
def manage_create_notification(**kwargs):
    notification = models.Notification.objects.create(
        receiver_id=kwargs['receiver_id'],  # Assign receiver ID from passed arguments
        text=kwargs['text'],  # Assign notification text
        media_url=kwargs.get('media_url'),  # Assign media URL if available, else None
        created_by=kwargs['created_by']  # Assign the creator of the notification
    )
    return notification  # Return the created notification instance


def get_notification_by_id(notification_id):
    """
    Retrieves a notification by its ID or raises a 404 error.

    Args:
        notification_id (int): The ID of the notification.

    Returns:
        Notification: The fetched notification instance.
    """
    return get_object_or_404(Notification, id=notification_id)

def update_notification(notification, cleaned_data, user):
    """
    Updates a notification's details.

    Args:
        notification (Notification): The notification instance to update.
        cleaned_data (dict): The cleaned form data.
        user (User): The user performing the update.

    Returns:
        Notification: The updated notification instance.
    """
    notification.text = cleaned_data['text']
    notification.media_url = cleaned_data.get('media_url')
    notification.receiver_id = user  # Assign the logged-in user
    notification.is_read = cleaned_data.get('is_read', notification.is_read)
    notification.save()
    return notification

def manage_list_notifications_filtered(search_query, sorting_order, sort_by, page_number):
    # get data
    data = (
        GetData(Notification)
        .search(search_query,"text","media_url","is_read")
        .sort(sort_by, sorting_order)
        .paginate(limit=10, page=page_number)
        .execute()
    )
    # return data
    return data


def toggle_notification_active_status(notification_id):
    """
    Toggles the active status of a notification and returns the updated status.

    Args:
        notification_id (int): The ID of the notification.

    Returns:
        bool: The updated active status of the notification.
    """
    notification = get_object_or_404(Notification, id=notification_id)  # Fetch the notification or return 404
    notification.is_active = not notification.is_active  # Toggle active status
    notification.save()  # Save changes
    return notification.is_active  # Return the updated status
