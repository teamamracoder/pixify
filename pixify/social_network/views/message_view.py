from django.shortcuts import render, redirect
from django.views import View

class MessageView(View):
    def get(self, request):
        return render(request, 'enduser/message/index.html')