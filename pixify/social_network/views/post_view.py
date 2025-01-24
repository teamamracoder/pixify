import json
import os
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

from social_network.services import post_reaction_service # type: ignore
from ..decorators import auth_required, role_required
from social_network.decorators.exception_decorators import catch_error
from social_network.constants.default_values import Role

from pixify import settings
from .. import services
from ..models import User,Comment,Post,PostReaction
from django.core.paginator import Paginator



from datetime import datetime, timedelta, timezone
from django.utils.timezone import now


def time_ago(dt):
    now = datetime.now(timezone.utc)
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours ago"
    elif seconds < 604800:
        return f"{int(seconds // 86400)} days ago"
    else:
        return f"{int(seconds // 604800)} weeks ago"
    
    
    
        
# use ajax post create
class UserPostCreatView(View):
    def get(self, request):
        return render(request, 'enduser/home/index.html')
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request):
            user_id =request.user.id
            print(user_id)
            post_Title = request.POST.get('postTitle')
            postFiles = request.FILES.getlist('postFiles')
            media_urls = []

            for file in postFiles:
                file_path = os.path.join(settings.MEDIA_ROOT, file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                media_urls.append(f"{settings.MEDIA_URL}{file.name}")

            services.post_service.user_post(post_Title, media_urls, user_id)
            return JsonResponse({'success': True, 'redirect_url': reverse('home')})
     

class UserPostDetail(View):
    def get(self, request, post_id):
         comment_dic= {
         'post' : services.post_service.get_post(post_id),
         'comment': services.comment_service.comments_filtered(post_id)
                   }
         return render(request, 'enduser/home/index.html', {'comment_dic':comment_dic})



class UserPostListView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self, request):
        posts = services.post_service.Postlist_posts()
        user_id = request.user.id
        post_dict = {
            'posts': posts,
            'user_id': user_id,
            'name': 'priya',
            'count_comment': services.comment_service.get_count_comment(163)
        }
        
        # Check if the request is an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(post_dict, safe=False)  # JSON response for AJAX requests
        
        # Render the page with the initial HTML
        return render(request, 'enduser/home/index.html', {'post_dict': post_dict})


# def create_reaction(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             post_id = data.get('postId')
#             reaction_id = data.get('reactionId')
#             reaction_value = data.get('reactionValue')
#             user = request.user

#             # Get the existing reaction
#             reaction = PostReaction.objects.get(post_id=post_id, created_by=user)

#             # Update the reaction
#             reaction.reaction_id = reaction_id
#             reaction.reaction_value = reaction_value
#             reaction.save()

#             return JsonResponse({'status': 'success', 'message': 'Reaction updated successfully!'})
#         except PostReaction.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Reaction not found'}, status=404)
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt  # Temporarily disable CSRF protection for testing
def create_reaction(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            post_id = data.get('postId')
            reaction_id = data.get('reactionId')
            reaction_value = data.get('reactionValue')
            # Perform logic to handle the reaction
            return JsonResponse({'status': 'success', 'message': 'Reaction added successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'}, status=405)


class UserPostEditView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self,request):
         post_id = request.GET.get('post_id')
         post_detail =list(services.post_service.get_post(post_id).values())
         return JsonResponse({'success': True, 'message': 'Title updated successfully.','post_detail':list(post_detail) })

    def post(self, request):
         user = request.user
         post_id = request.POST.get('post_id')
         post_title = request.POST.get('postTitle')
         print("post id is",post_id, "post titile",post_title)

         if not post_id or not post_title:
            return JsonResponse({'success': False, 'message': 'Missing post_id or postTitle'})

         post_update = services.post_service.update_post(user, post_id, post_title)
         print("post id is",post_update)
         return JsonResponse({'success': True})


        

        
    

    

