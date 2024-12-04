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

# def time_ago(time):
#     diff = now() - time
#     seconds = diff.total_seconds()
#     minutes = seconds // 60
#     hours = minutes // 60
#     days = hours // 24

#     if seconds < 60:
#         return "just now"
#     elif minutes < 60:
#         return f"{int(minutes)}m"
#     elif hours < 24:
#         return f"{int(hours)}h"
#     elif days < 7:
#         return f"{int(days)}d"
#     else:
#         return time.strftime('%b %d, %Y')
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
    
    
class AdminPostListView(View):
    def get(self, request):
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', 'posted_by')
        sort_order = request.GET.get('sort_order', 'asc')
        page_number = request.GET.get('page', 1)


        # Adjust sort order for descending order
        if sort_order == 'desc':
            sort_by = '-' + sort_by

        print(f"Search Query: {search_query}")
        # Get filtered and sorted users based on search
        posts = services.post_service.admin_list_posts_filtered(search_query, sort_by)

        # Paginate the users
        paginator = Paginator(posts, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)

        # choices_gender = [{gender.value: gender.name} for gender in Gender]

        return render(request, 'adminuser/post/list.html', {
            'posts': page_obj,
            # 'choices_gender': choices_gender,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })

class AdminPostCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/post/create.html')

    def post(self, request):
        post_data = {
                    'posted_by': User.objects.get(id=request.POST['posted_by']),
                    'created_by': User.objects.get(id=request.POST['posted_by'])
                    # 'type': request.POST['type'],
                    # 'content_type': request.POST['content_type'],
                    # 'media_url': request.POST.get('media_url', ''),
                    # 'title': request.POST['title'],
                    # 'description': request.POST['description'],
                    # 'accessability': request.POST['accessability'],
                    # 'members': request.POST.getlist('members'),
                    # 'treat_as': request.POST['treat_as'],
                    # 'is_active': request.POST.get('is_active', 'on') == 'on'
                }
        services.post_service.create_post(**post_data)
        # return redirect(request,'adminuser/post/create.html')
        return redirect('post_list')


class AdminPostDetailView(View):
    def get(self, request, post_id):
        post = services.post_service.get_post(post_id)
        return render(request, 'adminuser/post/detail.html', {'post': post})

class AdminPostUpdateView(View):
    def get(self, request, post_id):
        post = services.post_service.get_post(post_id)
        return render(request, 'adminuser/post/update.html', {'post': post})

    def post(self, request, post_id):
        post = services.post_service.get_post(post_id)
        title = request.POST['title']
        description = request.POST['description']
        services.post_service.update_post(post, title, description)
        return redirect('post_detail', post_id=post.id)

class AdminPostDeleteView(View):
    def get(self, request, post_id):
        post = services.post_service.get_post(post_id)
        return render(request, 'adminuser/post/delete.html', {'post': post})

    def post(self, request, post_id):
        post = services.post_service.get_post(post_id)
        services.post_service.delete_post(post)
        return redirect('post_list')

class AdminTogglePostActiveView(View):
    def post(self, request, post_id):
        post = services.post_service.get_post(post_id)
        post.is_active = not post.is_active  # Toggle active status
        post.save()
        return JsonResponse({'is_active': post.is_active})




# create post for enduser 
class UserPostCreatView(View):
    def get(self, request):
        return render(request, 'enduser/home/index.html')

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
        return redirect('Userposts_list')
        




# display post for enduser create by priya
class UserPostListView(View):
    def get(self, request):
        
        posts = services.post_service.Postlist_posts()
        
        post_dict={
                  'posts':posts,
                  'name':'priya',
                  'count_commnet' :services.comment_service.get_count_comment()
                }
        return render(request, 'enduser/home/index.html', {'post_dict': post_dict})
    
    

# class UserPostDetail(View):
#     def get(self, request, post_id):
#          comment_dic= {
#          'post' : services.post_service.get_post(post_id),
#          'comment': services.comment_service.comments_filtered(post_id)
#                    }
#          return render(request, 'enduser/home/index.html', {'comment_dic':comment_dic})


        
