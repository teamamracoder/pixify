from django.shortcuts import render, redirect
from django.views import View

class AdminHomeView(View):
    def get(self, request):
        return render(request, 'adminuser/home/index.html')
