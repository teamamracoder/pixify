from django.shortcuts import render, redirect
from django.views import View

class EnduserprofileView(View):
    def get(self, request):
        return render(request, 'enduser/profile/index.html')