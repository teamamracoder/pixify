import datetime
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from .. import services
from ..models import User
from django.core.paginator import Paginator    
from django.http import JsonResponse

class PostListView(View):
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
        posts = services.post_service.list_posts_filtered(search_query, sort_by)

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

class PostCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/post/create.html')

    def post(self, request):
        post_data = {
                    'posted_by': User.objects.get(id=request.POST['posted_by']),
                    'type': request.POST['type'],
                    'content_type': request.POST['content_type'],
                    'media_url': request.POST.get('media_url', ''), 
                    'title': request.POST['title'],
                    'description': request.POST['description'],
                    'accessability': request.POST['accessability'],
                    'members': request.POST.getlist('members'),  
                    'treat_as': request.POST['treat_as'],
                    'is_active': request.POST.get('is_active', 'on') == 'on'
                }
        services.post_service.create_post(**post_data) 
        return redirect(request,'adminuser/post/create.html') 
        # return redirect(request,'adminuser/post/list.html')
                

class PostDetailView(View):
    def get(self, request, post_id):
        post = services.post_service.get_post(post_id)
        return render(request, 'adminuser/post/detail.html', {'post': post})

class PostUpdateView(View):
    def get(self, request, post_id):
        post = services.post_service.get_post(post_id)
        return render(request, 'adminuser/post/update.html', {'post': post})

    def post(self, request, post_id):
        post = services.post_service.get_post(post_id)
        title = request.POST['title']
        description = request.POST['description']
        services.post_service.update_post(post, title, description)
        return redirect('post_detail', post_id=post.id)

class PostDeleteView(View):
    def get(self, request, post_id):
        post = services.post_service.get_post(post_id)
        return render(request, 'adminuser/post/delete.html', {'post': post})

    def post(self, request, post_id):
        post = services.post_service.get_post(post_id)
        services.post_service.delete_post(post)
        return redirect('post_list')
    

class TogglePostActiveView(View):
    def post(self, request, post_id):
        post = services.post_service.get_post(post_id)
        post.is_active = not post.is_active  # Toggle active status
        post.save()
        return JsonResponse({'is_active': post.is_active})


