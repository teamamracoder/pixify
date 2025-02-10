from django.shortcuts import render
from django.views import View

class callView(View):
    def get(self, request, call_id): 
        context = {'call_id': call_id}  
        return render(request, 'enduser/chat/ringing.html', context=context)