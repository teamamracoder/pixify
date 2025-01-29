from django.shortcuts import render
from django.views import View

class CallView(View):
    def get(self,request):
        context={}
        return render(request,'enduser/chat/call.html',context=context)