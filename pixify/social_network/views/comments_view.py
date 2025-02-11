

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
from ..models import User,Comment,CommentReaction
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

        user_details = list(services.comment_service.get_user(user_id).values())
        post_del = list(services.comment_service.get_post(post_id).values())
        comment_list = services.comment_service.comment_list(post_id)
        comment_count =services.comment_service.comment_count(post_id)
      
        for comment in comment_list:
           
            if 'comment_by' in comment and isinstance(comment['comment_by'], dict):
                comment['comment_by_first_name'] = comment['comment_by'].get('first_name', 'Unknown')
                comment['comment_by_last_name'] = comment['comment_by'].get('last_name', 'Unknown')
           

        return JsonResponse({
            "status": "success",
            "comments": list(comment_list), 
            "posts": list(post_del),
            "user_details": list(user_details),
            "comment_count":comment_count,
        })






class GetPostCommentView(View):
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        user_id = request.user.id
        total_count = Comment.objects.filter(post_id_id=post_id, is_active=True).count()

        return JsonResponse({
            'total_count': total_count,

        })


 

class CommentReplyView(View):
    def post(self, request):  
        post_id = request.POST.get('post_id')
        comment_id = request.POST.get('reply_for')  # Can be empty for top-level comments
        user_id = request.user.id
        reply_text = request.POST.get('reply_text')


        comment_list = services.comment_service.comment_list(post_id)
        
        if not reply_text or not post_id:
            return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)
        try:
          
            if comment_id:  
                services.comment_service.user_reply_create(reply_text, post_id, user_id, comment_id)
                reply_list = list(comment_service.reply_list(comment_id).values())
           
            else:
              services.comment_service.user_comments_create(reply_text,post_id,user_id)
              reply_list = []
         
            return JsonResponse({
                "status": "success",
                "comments":list(comment_list),
                "replies": list(reply_list),
                
                
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


class DeleteCommentView(View):
    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get("comment_id")
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return JsonResponse({"success": True})
        except Comment.DoesNotExist:
            return JsonResponse({"success": False, "error": "Comment not found."})

        return JsonResponse({"success": False, "error": "Invalid request."})



class ToggleLikeView(View):
    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get("comment_id")
        comment = Comment.objects.get(id=comment_id)
        user_id=request.user.id
       

        created =services.comment_service.create_reaction(comment_id,user_id)

        # if not created:
        #     reaction.delete()  # Remove like if it already exists (toggle behavior)
        #     liked = False
        # else:
        #     liked = True

         #like_count = CommentReaction.comment_id_id.count()  # Count total likes
        #, "like_count": like_count
        return JsonResponse({"success": True})






class GetRepliesView(View):
    def get(self, request):
        comment_id = request.GET.get('comment_id')
       
        
        # Fetch only replies where reply_for_id matches the comment_id
        replies = Comment.objects.filter(reply_for_id=comment_id).values(
            'id', 'comment', 'comment_by__first_name', 'comment_by__last_name', 'created_at'
        )
        reply_count = replies.count()  # Count number of replies
        
        return JsonResponse({'replies': list(replies), 'reply_count': reply_count})





