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
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils.timezone import now
import os

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






class UserPostCreatView(View):
    def get(self, request):
        return render(request, 'enduser/home/index.html')

    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request):
        user_id = request.user.id
        post_Title = request.POST.get('postTitle')
        postFiles = request.FILES.getlist('postFiles')  # Get list of uploaded files

        IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        VIDEO_EXTENSIONS = ['.mp4', '.webm', '.avi', '.mov']

        media_urls = []

        for file in postFiles:
            file_extension = os.path.splitext(file.name)[1].lower()
            unique_timestamp = now().strftime('%Y%m%d%H%M%S')
            file_name = f"{unique_timestamp}_{file.name}"

            # Save all files directly in /media/
            file_path = file_name

            saved_path = default_storage.save(file_path, file)

            media_urls.append(f"{settings.MEDIA_URL}{saved_path}")
            if file_extension in VIDEO_EXTENSIONS:
                content_type = 3
                type=3
            elif file_extension in IMAGE_EXTENSIONS:
                content_type = 2
                type=1
            else:
                content_type = 1
                type=1

        if not media_urls:
            return JsonResponse({'success': False, 'error': 'No files uploaded'}, status=400)

        # Debugging: Print to console to verify the stored URLs


        # Store the post in the database
        post = Post.objects.create(
            title=post_Title,
            media_url=media_urls,  # Store as a list
            posted_by_id=user_id,
            created_by_id=user_id,
            type=type,
            content_type=content_type
        )

        return JsonResponse({'success': True, 'redirect_url': reverse('home')})






class UserPostDetail(View):
    def get(self, request, post_id):
         comment_dic= {
         'post' : services.post_service.get_post(post_id),
         'comment': services.comment_service.comments_filtered(post_id)
                   }
         return render(request, 'enduser/home/index.html', {'comment_dic':comment_dic})




class UpdatePostReactionView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        reaction_id = request.POST.get('reaction_id')

        user_id = request.user.id

        react=services.post_reaction_service.getemoji(reaction_id)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        existing_reaction = PostReaction.objects.filter(post_id_id=post, reacted_by_id=user_id,
                                          created_by_id= user_id,is_active= True).first()

        if existing_reaction:
            existing_reaction.master_list_id_id = reaction_id
            existing_reaction.save()
        else:


           services.post_reaction_service.create_post_reaction(post_id,user_id,reaction_id)

        user_reaction = PostReaction.objects.filter(post_id_id=post_id, reacted_by_id=user_id, is_active=True).first()

        if user_reaction:
            react_id = user_reaction.master_list_id_id  # Get the reaction ID (react_id_id)
        else:
            react_id = None  # No reaction found for the user

        # Get total reaction count
        total_count = PostReaction.objects.filter(post_id_id=post, is_active=True).count()

        # Get the names of users who reacted
        user_reactions = list(services.post_reaction_service.post_reactionby_name(post).values())
        user_ids = [reaction['reacted_by_id'] for reaction in user_reactions]
        users = list(User.objects.filter(id__in=user_ids).values_list('first_name', 'last_name'))
        users = [f"{first} {last}" for first, last in users]



        new_reaction_count = PostReaction.objects.filter(post_id_id=post, is_active=True).count()

        return JsonResponse({
                             'new_reaction_count': new_reaction_count,
                             'reaction_id': reaction_id,
                             'total_count': total_count,
                             'reaction_name': users,
                             'user_reaction_id': react_id  # Include the user's reaction ID in the response
                             })



class GetPostReactionsView(View):
    def get(self, request, *args, **kwargs):
        post_id = request.GET.get('post_id')
        user_id = request.user.id
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        # Fetch the user's reaction for the post
        user_reaction = PostReaction.objects.filter(post_id_id=post_id, reacted_by_id=user_id, is_active=True).first()

        if user_reaction:
            react_id = user_reaction.master_list_id_id  # Get the reaction ID (react_id_id)
        else:
            react_id = None  # No reaction found for the user

        # Get total reaction count
        total_count = PostReaction.objects.filter(post_id_id=post, is_active=True).count()

        # Get the names of users who reacted
        user_reactions = list(services.post_reaction_service.post_reactionby_name(post).values())
        user_ids = [reaction['reacted_by_id'] for reaction in user_reactions]
        users = list(User.objects.filter(id__in=user_ids).values_list('first_name', 'last_name'))
        users = [f"{first} {last}" for first, last in users]

        return JsonResponse({
            'total_count': total_count,
            'reaction_name': users,
            'user_reaction_id': react_id  # Include the user's reaction ID in the response
        })


class UserPostEditView(View):
    @catch_error
    @auth_required
    @role_required(Role.ADMIN.value, Role.END_USER.value)
    def get(self,request):
         post_id = request.GET.get('post_id')
         user_id = request.GET.get('user_id')
         User_del=list(services.user_service.filter_user(user_id).values())
         print(User_del)
         post_detail =list(services.post_service.get_post(post_id).values())
         return JsonResponse({'success': True, 'message': 'Title updated successfully.','post_detail':list(post_detail),'User_del':list(User_del) })

    def post(self, request):
         user = request.user
         post_id = request.POST.get('post_id')
         post_title = request.POST.get('postTitle')

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


class Fetch_reactions(View):
    def get(self,request):
         post_id = request.GET.get('post_id')
         user_id = request.GET.get('user_id')
         reaction_id = request.GET.get('emoji_id')

         react=list(services.post_reaction_service.getemoji(reaction_id).values())
         return JsonResponse({'success': True,'react':react})


class remove_reaction(View):
     def get(self,request):
        post_id = request.POST.get("post_id")

        reaction = get_object_or_404(PostReaction, post_id_id=post_id)
        reaction.delete()

        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



class DeletePostReactionView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        user_id = request.user.id

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)

        # Find existing reaction by the user
        reaction = PostReaction.objects.filter(post_id=post, reacted_by_id=user_id, is_active=True).first()

        if reaction:
            reaction.delete()  # Delete the reaction
        else:
            return JsonResponse({'success': False, 'error': 'Reaction not found'}, status=404)

        # Get updated reaction count
        total_count = PostReaction.objects.filter(post_id=post, is_active=True).count()

        return JsonResponse({'success': True, 'total_count': total_count})
