<<<<<<< HEAD
import os
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from pixify import settings
from .. import services
from ..models import User
from django.core.paginator import Paginator




class UserPostCreatView(View):
    def post(self, request):
        user_id = 1;
        post_Title = request.POST['postTitle']
        postFiles = request.FILES.getlist('postFiles')
        postFile = []
        for file in postFiles:
            postFile.append(file.name)
        media_urls=[]
        for file in postFiles:
            file_path=os.path.join(settings.MEDIA_ROOT,file.name)
            with open(file_path,'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            media_urls.append(f"{settings.MEDIA_URL}{file.name}")


        services.post_service.user_post(post_Title,media_urls,user_id)
        return redirect('home')

# class UserPostCreateView(View):
#     def get(self, request):
#         return render(request, 'enduser/home/index.html')

#     def post(self, request):
#         post_Title = request.POST['postTitle']
#         postFiles = request.FILES.getlist('postFiles')
#         postFile = []
#         for file in postFiles:
#             postFile.append(file.name)
#         media_urls=[]
#         for file in postFiles:
#             file_path=os.path.join(settings.MEDIA_ROOT,file.name)
#             with open(file_path,'wb+') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)
#             media_urls.append(f"{settings.MEDIA_URL}{file.name}")


#         services.post_service.user_post(post_Title, media_urls)
#         return redirect('home')
=======
>>>>>>> 339241cfdc240eebedbec45d5f5ead4bf098398a
