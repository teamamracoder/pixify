from django.shortcuts import render
from django.views import View

from social_network.constants.default_values import Role
from social_network.decorators.exception_decorators import catch_error
from social_network.utils.common_utils import print_log

from ..decorators import auth_required, role_required

class HomeView(View):

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        return render(request, 'enduser/home/index.html')
