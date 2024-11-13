
from django.shortcuts import render, redirect
from django.views import View
from .. import services
from ..models import Notification

class NotificationListView(View):
    def get(self, request):
        notifications = services.admin_notification_service.list_notifications()
        return render(request, 'adminuser/notification/list.html',{'notifications':notifications})
    

class NotificationCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/notification/create.html')
  
    
    def notification(self, request):
        notification_data = {
            'receiver_id': Notification.objects.get(id=request.POST['receiver_id']),
            'text': request.POST['text'],           
            'media_url': request.POST.get('media_url', ''), 
            'is_read': request.POST['is_read'],            
            # 'is_active': request.POST.get('is_active', 'on') == 'on'
        }
        services.admin_notification_service.create_notifications(**notification_data) 
        return redirect(request,'adminuser/notification/create.html') 
         



class NotificationDetailView(View):
    def get(self, request, notification_id):
        notification = services.admin_notification_service.get_notification(notification_id)
        return render(request, 'adminuser/notification/detail.html',{'notification': notification})

# class NotificationUpdateView(View):
#     def get(self, request):
#         # services.admin_notification_service.get_notification()
#         return render(request, 'adminuser/notification/update.html')

#     def post(self, request, post_id):
#         notification = services.admin_notification_service.get_notification()
#         text = request.POST['text']
#         media_url = request.POST['media_url']
#         receiver_id = request.POST['receiver_id']
#         is_read = request.POST['is_read']
#         notification = services.admin_notification_service.update_notification(notification, text, media_url, receiver_id, is_read,)
#         return redirect('notification_detail')

    


# class NotificationDeleteView(View):
#     def get(self, request):
#         return render(request, 'adminuser/notification/delete.html')   

    
    # def post(self, request):
    #     notification = services.notification_service.get_notification()
    #     notification = services.delete_notification_service.delete_notifications(notification)
    #     return redirect('notification_list')
    



