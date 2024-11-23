from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View 
from .. import services
from ..models import Notification
from django.core.paginator import Paginator
from ..constants.default_values import SortingOrder
from ..decorators.exception_decorators import catch_error
from ..decorators import auth_required, role_required
from ..packages.response import success_response
from ..forms.manage_notification_forms import ManageNotificationCreateForm, ManageNotificationUpdateForm
    
class ManageNotificationListView(View):
    @catch_error
    def get(self, request):
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', "created_at")
        sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
        page_number = request.GET.get('page', 1)

        # get data
        data = services.manage_notification_service.manage_list_notifications_filtered(
            search_query=search_query,
            sort_by=sort_by,
            sorting_order=sort_order,
            page_number=page_number
        )
        return render(
            request,
            'adminuser/notification/list.html',
            success_response("Notification data fetched successfully", data)
        ) 

class ManageNotificationDetailView(View):
    def get(self, request, notification_id):
        notification = services.manage_notification_service.manage_get_notification(notification_id)
        return render(request, 'adminuser/notification/detail.html',{'notification': notification})

class ManageNotificationCreateView(View):
    @catch_error
    def get(self, request):
        form = ManageNotificationCreateForm()
        return render(request, 'adminuser/notification/create.html', {"form": form})

    # @catch_error
    def post(self, request):
        user=request.user
        # if request.method == 'POST':
        form = ManageNotificationCreateForm(request.POST)
        if form.is_valid():
            notification_data = {
                'text': form.cleaned_data['text'],
                'media_url': form.cleaned_data['media_url'],
                'is_read': form.cleaned_data['is_read'],
                'receiver_id':user,              
                'created_by': user
            }
            services.manage_notification_service.manage_create_notification(**notification_data)
            return redirect('manage_notification_list')
        return render(request, 'adminuser/notification/create.html', {"form": form})

class ManageNotificationUpdateView(View):
    @catch_error
    def get(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)  # Assuming you have a User model
        form = ManageNotificationUpdateForm(initial={
            'text': notification.text,
            'media_url': notification.media_url,
            'receiver_id': notification.receiver_id.id,
            'is_raed': notification.is_read          
        })
        return render(request, 'adminuser/notification/update.html', {"form": form, "notification_id": notification.id})

    @catch_error
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        form = ManageNotificationUpdateForm(request.POST)
        if form.is_valid():
            notification.text = form.cleaned_data['text']
            notification.media_url = form.cleaned_data.get('media_url')
            # notification.receiver_id = form.cleaned_data['receiver_id']
            # notification.is_raed = form.cleaned_data['is_raed']            
            notification.save()  # Save the updated user instance

            return redirect('manage_notification_list')
        return render(request, 'adminuser/notification/update.html', {"form": form, "notification_id": notification.id})

class ManageToggleNotificationActiveView(View):
     def post(self, request, notification_id):
        notification = services.manage_notification_service.manage_get_notification(notification_id)
        notification.is_active = not notification.is_active  
        notification.save()
        return JsonResponse({'is_active': notification.is_active})  