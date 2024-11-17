from django.shortcuts import render, redirect
from django.views import View
from .. import services
from ..models import User
from django.core.paginator import Paginator    
from django.http import JsonResponse

class NotificationListView(View):
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
        notifications = services.admin_notification_service.list_notifications_filtered(search_query, sort_by)

        # Paginate the users
        paginator = Paginator(notifications, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)

        # choices_gender = [{gender.value: gender.name} for gender in Gender]

        return render(request, 'adminuser/notification/list.html', {
            'notifications': page_obj,
            # 'choices_gender': choices_gender,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })


# class NotificationListView(View):
#     def get(self, request):
#         notifications = services.admin_notification_service.list_notifications()
#         return render(request, 'adminuser/notification/list.html',{'notifications':notifications})
    

class NotificationCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/notification/create.html')
  
    
    def post(self, request):
        notification_data = {
            'receiver_id': User.objects.get(id=request.POST['receiver_id']),
            'text': request.POST['text'],           
            'media_url': request.POST.get('media_url', ''), 
            'is_read': request.POST['is_read']     
            
        }
        services.admin_notification_service.create_notifications(**notification_data) 
        # return redirect(request,'adminuser/notification/list.html') 
        return redirect('notification_list')         

class NotificationDetailView(View):
    def get(self, request, notification_id):
        notification = services.admin_notification_service.get_notification(notification_id)
        return render(request, 'adminuser/notification/detail.html',{'notification': notification})


class NotificationUpdateView(View):
    def get(self, request, notification_id):
        notification = services.admin_notification_service.get_notification(notification_id)
        return render(request, 'adminuser/notification/update.html',{'notification': notification})
    
    def post(self, request, notification_id):
        notification = services.admin_notification_service.get_notification(notification_id)

        notification_data = {
            'id' : notification.id,           
            'receiver_id': User.objects.get(id=request.POST['receiver_id']),
            'text': request.POST['text'],           
            'media_url': request.POST.get('media_url', ''), 
            'is_read': request.POST['is_read']     
        }
        services.admin_notification_service.update_notifications(**notification_data) 
        return redirect(request,'adminuser/notification/list.html')



class NotificationDeleteView(View):
    def get(self, request, notification_id):
        notification = services.admin_notification_service.get_user(notification_id)
        return render(request, 'adminuser/notification/delete.html', {'notification': notification})

    def post(self, request, notification_id):
        notification = services.admin_notification_service.get_notification(notification_id)
        services.admin_notification_service.delete_notification(notification)
        return redirect(request,'notification_list')
    
  
class ToggleNotificationActiveView(View):
    def post(self, request, notification_id):
        notification = services.admin_notification_service.get_notification(notification_id)
        notification.is_active = not notification.is_active  # Toggle active status
        notification.save()
        return JsonResponse({'is_active': notification.is_active})