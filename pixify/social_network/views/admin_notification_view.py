
from django.shortcuts import render, redirect
from django.views import View
from .. import services

class NotificationListView(View):
    def get(self, request):
        notifications = services.admin_notification_service.list_notifications()
        return render(request, 'adminuser/notification/list.html', {'notifications': notifications})

class NotificationCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/notification/create.html')
    
    
    def post(self, request):
        text = request.POST['text']
        media_url = request.POST['media_url']
        receiver_id = request.POST['receiver_id']
        is_read = request.POST['is_read']
        services.admin_notification_service.create_notifications(text, media_url, receiver_id, is_read)
        return redirect('notification_list')
    
    
class NotificationDeleteView(View):
    def get(self, request):
        return render(request, 'adminuser/notification/delete.html')   

    
    def post(self, request):
        notification = services.notification_service.get_user()
        services.user_service.delete_notifications(notification)
        return redirect('notification_list')