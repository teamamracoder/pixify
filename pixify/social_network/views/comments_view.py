from django.shortcuts import render, redirect
from django.views import View
from ..services import comment_service
from .. import services
import os
from django.http import HttpResponseBadRequest, JsonResponse
from pixify import settings
from ..models import User
from django.core.paginator import Paginator



class CommentsCreateView(View):
    def get(self, request):
        return render(request, 'enduser/comments/index.html')
    def post(self,request):                
         user_id = request.user.id
         commentstext=request.POST['comment_text']
         
         services.comment_service.user_comments_create(commentstext,user_id)
         return redirect('comments')
    
# class Commentlistview(View):
#     comment_list=services.comment_service.comment_list()    


class CommentsListView(View):
     def get (self,request):
         comment_list=services.comment_service.comment_list()
         return render (request,'enduser/home/index.html',{'comment_list':comment_list})


     
 
       
   
  
   
    