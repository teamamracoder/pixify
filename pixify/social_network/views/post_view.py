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
        # try:
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

            # Call the service to save post data
            services.post_service.user_post(post_Title, media_urls, user_id)
            # return JsonResponse({ "status": True, })

            return JsonResponse({'success': True, 'redirect_url': reverse('home')})
        # except Exception as e:
           # return JsonResponse({'success': False, 'message': str(e)})

class UserPostDetail(View):
    def get(self, request, post_id):
         comment_dic= {
         'post' : services.post_service.get_post(post_id),
         'comment': services.comment_service.comments_filtered(post_id)
                   }
         return render(request, 'enduser/home/index.html', {'comment_dic':comment_dic})


class UserPostListView(View):
    def get(self, request):
        posts = services.post_service.Postlist_posts()
        post_dict = {
            'posts': posts,
            'name': 'priya',
             'count_commnet' :services.comment_service.get_count_comment(post_ids)
        }
        print("postss",posts)
        # Check if the request is an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(post_dict)
        return render(request, 'enduser/home/index.html', {'post_dict': post_dict})
    

# class UserPostReactionCreateView(View):
#     @catch_error
#     @auth_required
#     @role_required(Role.ADMIN.value, Role.END_USER.value)
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             post_id = data.get('post_id')
#             reaction_type = data.get('reaction_type')
#             user = request.user
           
           
#             reaction = post_reaction_service.post_reaction(reaction_id)
#             if not reaction:
#                 return JsonResponse({'success': False, 'error': 'Invalid reaction'}, status=400)
#             post_reaction_service.create_post_reaction(post_id, user, reaction)
#             new_count = post_reaction_service.get_reaction_count(post_id, reaction)
#             return JsonResponse({'success': True, 'new_count': new_count}, status=200)
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=400)

# def create_reaction(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             post_id = data.get('postId')
#             reaction_id = data.get('reactionId')
#             reaction_value = data.get('reactionValue')
#             user = request.user
#             print(user)
#             print(reaction_id)
#             print(post_id )
#             print(reaction_value)

#             if not post_id or not reaction_id or not reaction_value:
#                 return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

#             # Save reaction to the database (example logic)
#             PostReaction.objects.create(post_id_id=post_id,created_by=user )
#             # post_reaction_service.create_post_reaction(post_id , user, reaction_id)
#             return JsonResponse({'status': 'success', 'message': 'Reaction added successfully!'})
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def create_reaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('postId')
            reaction_id = data.get('reactionId')
            reaction_value = data.get('reactionValue')
            user = request.user

            # Debugging logs (optional, remove in production)
            print("User:", user)
            print("Reaction ID:", reaction_id)
            print("Post ID:", post_id)
            print("Reaction Value:", reaction_value)

            if not post_id or not reaction_id or not reaction_value:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            # Save reaction to the database
            PostReaction.objects.create(
                post_id_id=post_id,
                created_by=user,
                reacted_by=user,  # Ensure this field is provided    
            )

            return JsonResponse({'status': 'success', 'message': 'Reaction added successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
