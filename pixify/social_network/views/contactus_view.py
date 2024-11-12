from django.shortcuts import render, redirect
from django.views import View

class ContactUsView(View):
    def get(self, request):
        return render(request, 'enduser/contactus/index.html')
