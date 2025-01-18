

from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from social_network.constants.success_messages import SuccessMessage
from social_network.packages.response import success_response
from ..models.post_model import Post
from ..services import comment_service
from .. import services
import os
from django.http import HttpResponseBadRequest, JsonResponse
from pixify import settings
from ..models import User,Comment
from django.core.paginator import Paginator


from datetime import datetime, timedelta
from django.utils.timezone import now


def time_ago(time):
    diff = now() - time
    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60

    # Only return hours, even if the difference is in minutes or seconds
    if hours < 1:
        return f"{int(minutes)}m"  # For under 1 hour, show minutes
    elif hours < 24:
        return f"{int(hours)}h"  # For less than 24 hours, show hours
    else:
        return f"{int(hours)}h"  # Show hours even if it's over 24 hours



class CommentsCreateView(View):
    def get(self, request):
        return render(request, 'enduser/home/index.html')
    
    def post(self,request):  
         post_id = request.POST.get('post_id') 
         user_id = request.user.id
         user_details=list(services.comment_service.get_user(user_id).values())
      
         
         commentstext=request.POST['comment_text']    
         services.comment_service.user_comments_create(commentstext,post_id,user_id)

         post_del=list(services.comment_service.get_post(post_id).values())

         comment_list = services.comment_service.comment_list(post_id)
         return JsonResponse({ "status": "success", "comments":list(comment_list),"posts":list(post_del),"user_details":list(user_details)})
           
   


class CommentsListView(View):
     
    def get(self, request):
         post_id = request.GET.get('post_id') 
         user_id = request.GET.get('user_id')
         
         user_details=list(services.comment_service.get_user(user_id).values())
         
         
   
         post_del=list(services.comment_service.get_post(post_id).values())
      
         comment_list = services.comment_service.comment_list(post_id)
         return JsonResponse({ "status": "success", "comments":list(comment_list),"posts":list(post_del),"user_details":list(user_details)})

