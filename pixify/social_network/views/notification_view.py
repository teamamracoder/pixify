from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View 

from .. import services
from ..models import User
from django.core.paginator import Paginator 

# end-user notification
class notificationView(View):
    def get(self, request):
        return render(request, 'enduser/notification/index.html')
    

