from django.shortcuts import render, redirect
from django.views import View

class messageView(View):
    def get(self, request):
        return render(request, 'enduser/message/index.html')