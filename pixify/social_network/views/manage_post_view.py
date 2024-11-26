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
from social_network.packages.response import success_response
from social_network.constants.default_values import SortingOrder



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
                    'created_by' : user,  # curent user
                    'type': form.cleaned_data['type'],
                    'content_type': form.cleaned_data['content_type'],
                    'title': form.cleaned_data['title'],
                    'description': form.cleaned_data['description'],
                    'accessability': form.cleaned_data['accessability'],
                    'treat_as': form.cleaned_data['treat_as']
                }
             services.post_service.manage_create_post(**post_data) 
             return redirect('manage_post_list')
        return render(request, 'adminuser/post/create.html', {"form": form})


class ManagePostListView(View):
    def get(self, request):
        # Fetch the search query from the URL parameters
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', "created_at")
        sort_order = request.GET.get('sort_order', SortingOrder.DESC.value)
        page_number = request.GET.get('page', 1)

        # get data
        data = services.post_service.manage_list_posts_filtered(
            search_query=search_query,
            sort_by=sort_by,
            sorting_order=sort_order,
            page_number=page_number
        )
        # return
        # print(data)
        # posted_by = services.post_service.manage_get_user(data.posted_by_id)
        return render(request,
            'adminuser/post/list.html',
            success_response("post data fetched successfully", data)
        ) 

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