from django.shortcuts import render
from django.views import View
from ..decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role
from ..decorators import auth_required, role_required

class CallView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request, call_id):
        template_name = 'enduser/chat/calling_feature.html'
        context = {
            'call_id': call_id,  # Pass the call_id to the template
        }
        return render(request, template_name, context)
