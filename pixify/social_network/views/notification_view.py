from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .. import services

 


class NotificationView(View):
    def get(self, request):
       notifications_fetch=services.user_Notification_service.count_notification()
       notification_list=list(notifications_fetch.values())
    #    notify={
    #          'notifications_fetch':notifications_fetch,
    #       }
       print(notification_list)
       return render(request, 'enduser/notification/index.html',{'notification_list':notification_list})
    
    
