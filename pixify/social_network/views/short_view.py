from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error

class ShortListView(View):
    def get(self, request):
        return render(request, 'enduser/short/index.html')
