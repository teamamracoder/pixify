from itertools import count
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
from ..models import User,Comment,Post,PostReaction,MasterList
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



# class UpdatePostReactionView(View):
#     def post(self, request, *args, **kwargs):
#         post_id = request.POST.get('post_id')
#         reaction_id = request.POST.get('reaction_id')
#         print("reaction_id",reaction_id)
#         user_id = request.user.id

#         post = Post.objects.get(id=post_id)
#         reaction =services.post_reaction_service.post_reactionby_name(post_id)
#         print("reaction",reaction)
        

#         # If no reaction exists, create one
#         if not reaction:
#             post_react=services.post_reaction_service.create_post_reaction(post_id,user_id)
#             #post_react=services.post_reaction_service.create_or_update_message_reaction(post_id,user_id)

#         # Count the new reaction
#         new_reaction_count = PostReaction.objects.filter(post_id_id=post_id, is_active=True).count()

#         return JsonResponse({'new_reaction_count': new_reaction_count})
class UpdatePostReactionView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        reaction_id = request.POST.get('reaction_id')
        print("reaction id new",reaction_id)
        user_id = request.user.id

        react=services.post_reaction_service.getemoji(reaction_id)
        print("afklakflafk",react)
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        # Check if the user has already reacted to the post
        existing_reaction = PostReaction.objects.filter(post_id_id=post, reacted_by_id=user_id,
                                          created_by_id= user_id,is_active= True).first()

        if existing_reaction:
            # If the user already reacted, update the reaction type
            existing_reaction.reaction_id = reaction_id
            existing_reaction.save()
        else:
            # If no reaction exists, create a new one
            #PostReaction.objects.create(post_id_id=post, reacted_by_id=user_id,created_by_id= user_id,is_active= True )
           services.post_reaction_service.create_post_reaction(post_id,user_id)
        # Count the new reaction
        new_reaction_count = PostReaction.objects.filter(post_id_id=post, is_active=True).count()

        return JsonResponse({'new_reaction_count': new_reaction_count,' reaction_id': reaction_id})


class GetPostReactionsView(View):
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        user_id = request.user.id
        print("a",post_id)
        try:
            post = Post.objects.get(id=post_id)

        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        # Get total reaction count
        total_count = PostReaction.objects.filter(post_id_id=post, is_active=True).count()

        # Get the current usr's reaction (if any)
        user_reaction = list(services.post_reaction_service.post_reactionby_name(post).values())

        # print("user name",user_reaction)
        # users = [reaction['reacted_by_id'] for reaction in user_reaction]
        user_ids = [reaction['reacted_by_id'] for reaction in user_reaction]

        users = list(User.objects.filter(id__in=user_ids).values_list('first_name', 'last_name'))
        users = [f"{first} {last}" for first, last in users]


        return JsonResponse({
            'total_count': total_count,
            'reaction_name':users,
   

        })



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




 # post reaction 
class PostReactionCreateView(View):
    def post(self, request):
        data = request.POST or request.json()
        post_id = data.get('post_id')
        reaction_id = data.get('reaction_id')

        post = get_object_or_404(Post, id=post_id)
        reaction_type = get_object_or_404(MasterList, id=reaction_id)

        # Check if the user already reacted to this post
        existing_reaction = PostReaction.objects.filter(post_id_id=post, reacted_by_id=request.user).first()

        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                return JsonResponse({'success': False, 'message': 'Already reacted'}, status=400)
            else:
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
        else:
            PostReaction.objects.create(post_id_id=post, reacted_by_id=request.user, created_by_id=request.user)

        return JsonResponse({'success': True})


class PostReactionDeleteView(View):
    def post(self, request):
        data = request.POST or request.json()
        post_id = data.get('post_id')

        post = get_object_or_404(Post, id=post_id)
        reaction = PostReaction.objects.filter(post_id_id=post, reacted_by_id=request.user).first()

        if reaction:
            reaction.delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Reaction not found'}, status=400)

class PostReactionsView(View):
    def get(self, request, post_id):

        reactions = PostReaction.objects.filter(post_id_id=post_id)
        print("new react",reactions)
        reaction_data = {}


        for reaction in reactions:
            reaction_type = reaction.reaction_id.value
            if reaction_type in reaction_data:
                reaction_data[reaction_type] += 1
            else:
                reaction_data[reaction_type] = 1

        return JsonResponse({'reactions': reaction_data}) 


class PostReactionsListView(View):

    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user = request.user  # Get the logged-in user

        # Get all reactions for the post
        reactions = PostReaction.objects.filter(post_id_id=post).select_related('reacted_by')

        # Get unique reaction counts
        reaction_data = {}
        user_reaction_id = None  # Store the current user's reaction

        for reaction in reactions:
            reacted_by = reaction.reacted_by
            reaction_type = MasterList.objects.filter(id=reaction.id).first()

            if reaction_type:
                reaction_id = reaction_type.id
                reaction_name = reaction_type.name
                reaction_icon = reaction_type.value  # Stores the emoji/icon HTML

                if reaction_id not in reaction_data:
                    reaction_data[reaction_id] = {
                        'name': reaction_name,
                        'icon': reaction_icon,
                        'count': 0
                    }
                reaction_data[reaction_id]['count'] += 1

                # Check if the current user reacted and store their reaction
                if reacted_by == user:
                    user_reaction_id = reaction_id

        return JsonResponse({
            'post_id': post.id,
            'reactions': list(reaction_data.values()),
            'user_reaction': user_reaction_id
        })