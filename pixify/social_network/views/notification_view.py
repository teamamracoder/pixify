from django.shortcuts import render, redirect
from django.views import View

class notificationView(View):
    def get(self, request):
        return render(request, 'enduser/notification/index.html')