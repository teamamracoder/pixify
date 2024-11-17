
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View 

from .. import services
from ..models import User
from django.core.paginator import Paginator 

from social_network.constants.default_values import Role
from social_network.decorators.exception_decorators import catch_error

from ..decorators import auth_required, role_required
from social_network.packages.response import success_response


    
class ManageNotificationListView(View):

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):     
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '') 
        sort_by = request.GET.get('sort_by', 'text')
        sort_order = request.GET.get('sort_order', 'asc')
        page_number = request.GET.get('page', 1)

        # Adjust sort order for descending order
        if sort_order == 'desc':
            sort_by = '-' + sort_by

        print(f"Search Query: {search_query}")
        # Get filtered and sorted users based on search
        notifications = services.manage_notification_service.manage_list_notifications_filtered(search_query, sort_by)

        # Paginate the users
        paginator = Paginator(notifications, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)

        return render(request, 'adminuser/notification/list.html', {
            'notifications': page_obj,
            # 'choices_gender': choices_gender,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })

class ManageNotificationCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/notification/create.html')
  
    def post(self, request):
        notification_data = {
            'receiver_id': User.objects.get(id=request.POST['receiver_id']),
            'created_by': User.objects.get(id=request.POST['created_by']),
            'text': request.POST['text'],           
            'media_url': request.POST.get('media_url', ''), 
            'is_read': request.POST['is_read']            

        }
        services.manage_notification_service.manage_create_notification(**notification_data)      
        return redirect('manage_notification_list')         

class ManageNotificationDetailView(View):
    def get(self, request, notification_id):
        notification = services.manage_notification_service.manage_get_notification(notification_id)
        return render(request, 'adminuser/notification/detail.html',{'notification': notification})

class ManageNotificationUpdateView(View):

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)  

    def get(self, request, notification_id):       
        notification = services.manage_notification_service.manage_get_notification(notification_id)
        return render(request, 'adminuser/notification/update.html', {'notification': notification})
    
    def post(self, request, notification_id):
        notification = services.manage_notification_service.manage_get_notification(notification_id)

        # Gather all form data into a dictionary
        notification_data = {
            'text': request.POST.get('text'),
            'media_url': request.POST.get('media_url'),
            'receiver_id': User.objects.get(id=request.POST['receiver_id']),
            'is_read': request.POST.get('is_read')           
        }

        # Validate required fields
        required_fields = ['text', 'media_url', 'receiver_id', 'is_read']
        for field in required_fields:
            if not notification_data.get(field):
                return HttpResponseBadRequest(f"Missing required field: {field}")

        # Update the user with the provided data
        services.manage_notification_service.manage_update_notification(
            notification, 
            **notification_data  # Pass the dictionary as keyword arguments
        )
        return redirect('manage_notification_detail', notification_id=notification.id)


class ManageToggleNotificationActiveView(View):

     def post(self, request, notification_id):
        notification = services.manage_notification_service.manage_get_notification(notification_id)
        notification.is_active = not notification.is_active  
        notification.save()
        return JsonResponse({'is_active': notification.is_active})  