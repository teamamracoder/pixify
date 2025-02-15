#story_view.py
import os
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from pixify import settings
from .. import services
from ..models import User,Post,User
from django.core.paginator import Paginator



from datetime import datetime, timedelta, timezone
from django.utils.timezone import now
from ..constants import PostContentType,PostType

class UserStoryCreatView(View):
    def post(self, request):
        user_id = request.user.id  # Replace with the logged-in user's ID
        storyFiles = request.FILES.getlist('story-input')
        music_file = request.FILES.get('music-input')
        text_content = request.POST.get('story-text', None)  # Fetch text content

        media_urls = []
        #media_types = []
        media_types=[]
        music_url = None

        # Process media files
        for file in storyFiles:
            file_extension = file.name.split('.')[1].lower()
            file_type = PostContentType.VIDEO.value if file_extension in ['mp4', 'mov', 'avi'] else PostContentType.PHOTO.value
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)

            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            media_urls.append(f"{settings.MEDIA_URL}{file.name}")
            media_types.append(file_type)
            #print("file_type",file_type)

        # Process music file
        if music_file:
            music_path = os.path.join(settings.MEDIA_ROOT, music_file.name)
            with open(music_path, 'wb+') as destination:
                for chunk in music_file.chunks():
                    destination.write(chunk)
            music_url = f"{settings.MEDIA_URL}{music_file.name}"

        # Save story data using the service
        if text_content:
            services.story_service.user_story(
                media_urls=[],
                media_types= PostContentType.TEXT.value,
                user_id=user_id,
                story_text=text_content,
            )
        else:
            services.story_service.user_story(
                media_urls, media_types, user_id, music_url=music_url
            )

        return redirect('home')

class UserstoryListView(View):
    def get(self, request, user_id=None):
        """
        If `user_id` is provided, fetch all stories by that user; otherwise, fetch all stories.
        """
        if user_id:
            user_stories = services.story_service.get_user_stories(user_id)
            return render(request, 'enduser/home/index.html', {'stories': user_stories})


        # Default behavior: Fetch all stories
        user_id= request.user.id
        stories = services.story_service.get_all_stories()
        latest_story = services.story_service.get_latest_story()
        story_dict = {
            'stories': stories,
            'latest_story': latest_story,
            'user_id': user_id,

        }
        return render(request, 'enduser/home/index.html', {'story_dict': story_dict,'stories': user_stories})


# class UserActiveStories(View):
#     def get(self, request, user_id):
#         user_stories = services.story_service.get_user_stories(user_id)
#         active_stories = [
#             {
#                 'media_url': story.media_url[0] if story.media_url else None,
#                 'media_type': story.media_type,
#                 'description': story.description,
#                 'posted_by': story.posted_by.id,
#             }
#             for story in user_stories
#         ]
#         print(active_stories)
#         return JsonResponse({'stories': active_stories})


class UserActiveStories(View):
    def get(self, request, user_id):
        """
        Fetch all stories grouped by user.
        """
        users_with_stories = (
            Post.objects.values("posted_by_id").distinct()
        )  # Get unique users with stories

        all_stories = {}

        for user in users_with_stories:
            user_id = user["posted_by_id"]
            user_stories = Post.objects.filter(posted_by_id=user_id,type=PostType.STATUS.value).order_by(
                "created_at"
            )  # Get all stories of the user

            all_stories[user_id] = [
                {
                    "media_url": story.media_url[0] if story.media_url else None,
                    "media_type": story.content_type,
                    "description": story.description,
                    "posted_by": story.posted_by.id,
                    "first_name": story.posted_by.first_name,
                    "last_name" : story.posted_by.last_name
                }
                for story in user_stories
            ]
        user_queryset = services.user_service.get_user_name_and_img(user_id=user_id)
        user_instance = user_queryset.first()
        print("user_instance",user_instance)
        if user_instance:
            user_details = {
                "first_name": user_instance.first_name,
                "profile_photo_url": user_instance.profile_photo_url,
            }
        else:
            user_details = None
        print("user_details",user_details)
        return JsonResponse({"stories": all_stories, "userDetails": user_details})



class UploadStoryView(View):
    def get(self, request):
        user = request.user  # Get the currently logged-in user
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_photo_url': user.profile_photo_url
        }
        print("dfdf",user_data)
        return render(request, 'enduser/story/uploadStory.html', {'user_data': user_data})
