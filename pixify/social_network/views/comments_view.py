from django.shortcuts import render, redirect
from django.views import View

class CommentsView(View):
    def get(self, request):
        return render(request, 'enduser/comments/index.html')
