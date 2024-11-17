from django.shortcuts import render, redirect
from django.views import View

class FriendRequestView(View):
    def get(self, request):
        return render(request, 'enduser/friendrequest/index.html')