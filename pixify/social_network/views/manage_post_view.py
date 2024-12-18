from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.views import View

from ..forms.manage_post_forms import ManagePostUpdateForm
from ..models.post_specific_user_model import PostSpecificUser
from ..forms.manage_user_forms import ManageUserCreateForm
from ..models.post_model import Post
from ..decorators.exception_decorators import catch_error
# from ..forms.manage_post_forms import ManagePostCreateForm, ManagePostUpdateForm, ManagePostSpecificUserForm
from .. import services
from ..models import User
from django.core.paginator import Paginator 
from django.http import HttpResponseBadRequest
from ..forms import ManagePostCreateForm

class ManagePostCreateView(View):
    @catch_error
    def get(self,request):
        form = ManagePostCreateForm()
        return render(request, 'adminuser/post/create.html', {"form": form})

    @catch_error
    def post(self, request):
        user = request.user
        form = ManagePostCreateForm(request.POST)
        if form.is_valid():
             post_data = {
                    'posted_by': User.objects.get(id=request.POST['posted_by']),
                    'created_by' : user,
                    # 'created_by': User.objects.get(id=request.POST['posted_by']),
                    'type': form.cleaned_data['type'],
                    'content_type': form.cleaned_data['content_type'],
                    # 'media_url': request.POST.get('media_url', ''), 
                    'title': form.cleaned_data['title'],
                    'description': form.cleaned_data['description'],
                    'accessability': form.cleaned_data['accessability'],
                    # 'members': request.POST.getlist('members'),  
                    'treat_as': form.cleaned_data['treat_as'],
                    # 'is_active': request.POST.get('is_active', 'on') == 'on'
                }
             services.post_service.manage_create_post(**post_data) 
             return redirect('manage_post_list')
        return render(request, 'adminuser/post/create.html', {"form": form})


class ManagePostListView(View):
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
        posts = services.post_service.manage_list_posts_filtered(search_query, sort_by)

        # Paginate the users
        paginator = Paginator(posts, 10)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)

        return render(request, 'adminuser/post/list.html', {
            'posts': page_obj,
            'sort_by': sort_by,
            'sort_order': sort_order,
            'search_query': search_query,  # Ensure this is being passed to the template
            'page_obj': page_obj,
        })

class ManagePostDetailView(View):
    def get(self, request, post_id):
        post = services.post_service.manage_get_post(post_id)
        return render(request, 'adminuser/post/detail.html', {'post': post,'post_id':post_id})
    

class ManagePostUpdateView(View):
    @catch_error
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)  
        form = ManagePostUpdateForm(initial={
            'title': post.title,
            'type': post.type,
            'description' : post.description,
            'posted_by': post.posted_by.id,
            'content_type': post.content_type,
            'accessability': post.accessability,
            'treat_as': post.treat_as
            
        })
        return render(request, 'adminuser/post/update.html', {"form": form, "post_id": post.id})

    @catch_error
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = ManagePostUpdateForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.type = form.cleaned_data['type']
            post.description = form.cleaned_data['description']
            post.content_type = form.cleaned_data['content_type']
            post.accessability = form.cleaned_data['accessability']
            post.treat_as = form.cleaned_data['treat_as']
            post.save()  
            return redirect('manage_post_list')
        return render(request, 'adminuser/post/update.html', {"form": form, "post_id": post.id})




class ManagePostDeleteView(View):
    def get(self, request, post_id):
        post = services.post_service.manage_get_post(post_id)
        return render(request, 'adminuser/post/delete.html', {'post': post})

    def post(self, request, post_id):
        post = services.post_service.manage_get_post(post_id)
        services.post_service.manage_delete_post(post)
        return redirect('manage_post_list')
    
class ManageTogglePostActiveView(View):
    def post(self, request, post_id):
        post = services.post_service.manage_get_post(post_id)
        post.is_active = not post.is_active  # Toggle active status
        post.save()
        return JsonResponse({'is_active': post.is_active})
    

