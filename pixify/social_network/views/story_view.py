
import os
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from pixify import settings
from .. import services
from ..models import User
from django.core.paginator import Paginator



from datetime import datetime, timedelta, timezone
from django.utils.timezone import now

# create story for enduser
class UserStoryCreatView(View):
    def get(self, request):
        return render(request, 'enduser/home/index.html')

    def post(self, request):
        user_id = 1
        # story_Title = request.POST['story-text']
        # story_Title = request.POST['story-text']
        storyFiles = request.FILES.getlist('story-input')
        storyFile = []
        for file in storyFiles:
            storyFile.append(file.name)
        media_urls=[]
        for file in storyFiles:
            file_path=os.path.join(settings.MEDIA_ROOT,file.name)
            with open(file_path,'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            media_urls.append(f"{settings.MEDIA_URL}{file.name}")


        services.story_service.user_story(media_urls,user_id)
        return redirect('home')
        #return render(request, 'enduser/home/index.html')





# display story for enduser create by priya
class UserstoryListView(View):
    def get(self, request):

        storys = services.story_service.storylist_storys()

        story_dict={
                  'storys':storys,
                  'name':'sribash',
                #   'count_commnet' :services.comment_service.get_count_comment()



                }
        print('storage',storys)
        return render(request, 'enduser/home/index.html', {'story_dict': story_dict})


class UploadStoryView(View):
    def get(self, request):
        return render(request, 'enduser/story/uploadStory.html')