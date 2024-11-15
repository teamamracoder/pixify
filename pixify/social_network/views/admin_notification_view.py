
from django.shortcuts import render, redirect
from django.views import View
from .. import services
from ..models import User

class NotificationListView(View):
    def get(self, request):
        notifications = services.admin_notification_service.list_notifications()
        return render(request, 'adminuser/notification/list.html',{'notifications':notifications})
    

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
        return redirect(request,'adminuser/notification/list.html')          

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

# class NotificationDeleteView(View):
#     def get(self, request):
#         return render(request, 'adminuser/notification/delete.html')  
        
#     def post(self, request):
#         notification = services.notification_service.get_notification()
#         notification = services.delete_notification_service.delete_notifications(notification)
#         return redirect('notification_list')
    



