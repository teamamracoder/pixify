from django.shortcuts import render, redirect
from django.views import View

class BirthdayView(View):
    def get(self, request):
        return render(request, 'enduser/birthday/index.html')