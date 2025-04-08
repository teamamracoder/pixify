# Import error messages from pyexpat.errors (not commonly used, consider using Django messages framework)
from pyexpat.errors import messages
from django.http import HttpResponseBadRequest, JsonResponse    # Import required Django modules for HTTP responses and redirection
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View 
from ..import services  # Import services module (assumed to contain business logic related to notifications)
from ..models import Notification   # Import Notification model
from django.core.paginator import Paginator     # Import Paginator for handling paginated lists of notifications
from ..constants.default_values import SortingOrder    # Import sorting order constants
from ..decorators.exception_decorators import catch_error   # Import custom decorators for handling exceptions and authentication/authorization
from ..decorators import auth_required, role_required
from ..packages.response import success_response    # Import response helper function to standardize API responses
from ..forms import ManageNotificationCreateForm, ManageNotificationUpdateForm  # Import form classes for creating and updating notifications


class ManageNotificationListView(View):
    @catch_error  # Decorator to catch and handle errors in the view
    def get(self, request):
        # Fetch the search query from the URL parameters (default is an empty string)
        search_query = request.GET.get('search', '')

        # Fetch sorting field from request parameters (default is 'created_at')
        sort_by = request.GET.get('sort_by', "created_at")

        # Fetch sorting order (default is descending)
        sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)

        # Fetch page number for pagination (default is page 1)
        page_number = request.GET.get('page', 1)

        # Fetch filtered notification data using the service function
        data = services.manage_notification_service.manage_list_notifications_filtered(
            search_query=search_query,  # Pass search query
            sort_by=sort_by,  # Pass sorting field
            sorting_order=sort_order,  # Pass sorting order
            page_number=page_number  # Pass page number for pagination
        )

        # Render the notification list page with fetched data and success response
        return render(
            request,  # Request object
            'adminuser/notification/list.html',  # Path to the template
            success_response("Notification data fetched successfully", data)  # Pass response message and data
        )


class ManageNotificationDetailView(View):  
    def get(self, request, notification_id):  
        # Fetch the notification details using the service function  
        notification = services.manage_notification_service.manage_get_notification(notification_id)  

        # Render the notification detail page and pass the notification object to the template  
        return render(request, 'adminuser/notification/detail.html', {'notification': notification})  


class ManageNotificationCreateView(View):
    @catch_error
    def get(self, request):
        # Initialize an empty form for creating a new notification
        form = ManageNotificationCreateForm()
        
        # Render the notification creation page with the empty form
        return render(request, 'adminuser/notification/create.html', {"form": form})

    def post(self, request):
        # Get the logged-in user (creator of the notification)
        user = request.user
        
        # Bind the POST data to the form
        form = ManageNotificationCreateForm(request.POST)
        
        # Check if the form data is valid
        if form.is_valid():
            # Prepare the notification data from the validated form inputs
            notification_data = {
                'text': form.cleaned_data['text'],  # Notification text
                'media_url': form.cleaned_data['media_url'],  # Optional media link
                'receiver_id': user,  # Set receiver as the logged-in user
                'created_by': user  # Track who created the notification
            }
            
            # Call the service function to create a notification in the database
            services.manage_notification_service.manage_create_notification(**notification_data)
            
            # Redirect the user to the notification list page after successful creation
            return redirect('manage_notification_list')

        # If form validation fails, render the page again with error messages
        return render(
            request,
            'adminuser/notification/create.html',
            success_response(
                message=messages  # Display validation messages
            ),
            {"form": form}
        )


class ManageNotificationUpdateView(View):
    """
    View to handle updating a notification.
    Provides both GET (to display the form) and POST (to process the update).
    """

    @catch_error
    def get(self, request, notification_id):
        """
        Handles GET requests to load the update form for a notification.

        Args:
            request (HttpRequest): The request object.
            notification_id (int): The ID of the notification to be updated.

        Returns:
            HttpResponse: Renders the notification update form.
        """
        # Fetch notification data using the service function
        notification = services.get_notification_by_id(notification_id)

        # Initialize the form with existing notification data
        form = ManageNotificationUpdateForm(initial={
            'text': notification.text,
            'media_url': notification.media_url,
            'receiver_id': notification.receiver_id.id,
            'is_raed': notification.is_read  
        })

        return render(request, 'adminuser/notification/update.html', {"form": form, "notification_id": notification.id})

    @catch_error
    def post(self, request, notification_id):
        """
        Handles POST requests to update a notification.

        Args:
            request (HttpRequest): The request object containing form data.
            notification_id (int): The ID of the notification being updated.

        Returns:
            HttpResponseRedirect: Redirects to the notification list on success.
            HttpResponse: Renders the update form again if validation fails.
        """
        user = request.user  # Get the logged-in user

        # Fetch the notification using the service function
        notification = services.get_notification_by_id(notification_id)

        # Populate the form with submitted data
        form = ManageNotificationUpdateForm(request.POST)

        if form.is_valid():
            # Update notification details using service function
            services.update_notification(notification, form.cleaned_data, user)

            return redirect('manage_notification_list')  # Redirect to notification list after success
        
        # Re-render the form with errors if validation fails
        return render(request, 'adminuser/notification/update.html', {"form": form, "notification_id": notification.id})
    

class ManageToggleNotificationActiveView(View):
    """
    View to toggle the active status of a notification.
    """

    def post(self, request, notification_id):
        """
        Handles POST request to toggle a notification's active status.

        Args:
            request (HttpRequest): The request object.
            notification_id (int): The ID of the notification to toggle.

        Returns:
            JsonResponse: A JSON response indicating the updated status.
        """
        # Call the service function to toggle the notification's active status
        is_active = services.toggle_notification_active_status(notification_id)

        return JsonResponse({
            'is_active': is_active,
            'message': 'Notification status updated successfully',
            'message_type': 'success'
        })
