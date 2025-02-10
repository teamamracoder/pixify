from django.shortcuts import render
from django.views import View
from ..decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required

class CallView(View):
    def get(self, request, call_id): 
        context = {'call_id': call_id}  
        return render(request, 'enduser/chat/ringing.html', context=context)
