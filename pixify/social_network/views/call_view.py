from django.shortcuts import render
from django.views import View

class MakeCallView(View):
    def get(self, request, page_type, call_id, chat_id):
        context = {
            'call_id': call_id,
            'chat_id': chat_id
        }
        if page_type == 'calling':
            return render(request, 'enduser/chat/calling.html', context=context)
        return render(request, 'enduser/chat/ringing.html', context=context)

class CallView(View):
    def get(self, request, call_id, chat_id):
        context = {
            'call_id': call_id,
            'chat_id': chat_id
        }
        return render(request, 'enduser/chat/call.html', context=context)
