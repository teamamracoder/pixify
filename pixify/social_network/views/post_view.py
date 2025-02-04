import json
import os
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
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



# class UserPostListView(View):
#     @catch_error
#     @auth_required
#     @role_required(Role.ADMIN.value, Role.END_USER.value)
#     def get(self, request):
        
#         posts = services.post_service.Postlist_posts()
#         print(posts)
#         user_id = request.user.id
#         post_dict = {
#             'posts': posts,
#             'user_id': user_id,
#             'name': 'priya',
#             'count_comment': services.comment_service.get_count_comment(163)
#         }
#         print(post_dict)
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse(post_dict, safe=False)  # JSON response for AJAX requests
#         return render(request, 'enduser/home/index.html', {'post_dict': post_dict})



class UpdatePostReactionView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        reaction_id = request.POST.get('reaction_id')
        user_id = request.user.id  # Assuming the user is logged in

        # Get the post and check for the existing reaction
        post = Post.objects.get(id=post_id)
        reaction =services.post_reaction_service.post_reactionby_name(reaction_id)
        print("reaction name",reaction)
        

        # If no reaction exists, create one
        if not reaction:
            # post_react=services.post_reaction_service.create_post_reaction(post_id,user_id)
            post_react=services.post_reaction_service.create_or_update_message_reaction(post_id,user_id)

        # Count the new reaction
        new_reaction_count = PostReaction.objects.filter(post_id_id=post_id, is_active=True).count()
        print(new_reaction_count)

        return JsonResponse({'new_reaction_count': new_reaction_count})



class UserPostEditView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self,request):
         post_id = request.GET.get('post_id')
         user_id = request.GET.get('user_id')
         User_del=list(services.user_service.filter_user(user_id).values())
         post_detail =list(services.post_service.get_post(post_id).values())
         return JsonResponse({'success': True, 'message': 'Title updated successfully.','post_detail':list(post_detail),'User_del':list(User_del) })

    def post(self, request):
         user = request.user
         post_id = request.POST.get('post_id')
         post_title = request.POST.get('postTitle')
         print("post id is",post_id, "post titile",post_title)

         if not post_id or not post_title:
            return JsonResponse({'success': False, 'message': 'Missing post_id or postTitle'})

         services.post_service.update_post(user, post_id, post_title)
         
         return JsonResponse({'success': True, 'message': 'Title updated successfully.' })


        
    

    

# class UserPostDeleteView(View):
#     def get(self,request):
#         post_id = request.POST.get('post_id')
#         post = services.post_service.get_post(post_id)
#         return render(request, 'enduser/home/index.html', {'post': post})


#     def post(self, request):
#         post_id = request.POST.get('post_id')
#         post = services.post_service.get_post(post_id)
#         services.post_service.delete_post(post)
#         return redirect('post_list')

class UserPostDeleteView(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'error': 'Post ID is required'}, status=400)

        post = services.post_service.get_post(post_id)
        if not post:
            return JsonResponse({'error': 'Post not found'}, status=404)

        services.post_service.delete_post(post)
        return JsonResponse({'message': 'Post deleted successfully'}, status=200)