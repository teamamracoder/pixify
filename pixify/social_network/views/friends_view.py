from django.shortcuts import render, redirect
from django.views import View

class FriendsView(View):
    def get(self, request):
        return render(request, 'enduser/friends/index.html')