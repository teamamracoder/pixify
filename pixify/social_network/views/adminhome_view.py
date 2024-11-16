from django.shortcuts import render, redirect
from django.views import View
from social_network.packages.response import success_response

class AdminHomeView(View):
    def get(self, request):
        session_message = request.session.pop('message','') 
        session_message_type = request.session.pop('message_type','') 
        return render(request, 'adminuser/home/index.html', success_response(session_message, message_type=session_message_type))
