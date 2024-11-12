from django.shortcuts import render, redirect
from django.views import View

class NotificationView(View):
    def get(self, request):
        return render(request, 'enduser/notification/index.html')