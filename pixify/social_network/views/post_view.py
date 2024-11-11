from django.shortcuts import render, redirect
from django.views import View
from .. import services


class PostListView(View):
    def get(self, request):
        
        posts = services.post_service.list_posts()
        return render(request, 'adminuser/post/list.html', {'posts': posts})

class PostCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/post/create.html')

    def post(self, request):
        title = request.POST['title']
        description = request.POST['description']
        services.post_service.create_post(title, description)
        return redirect('post_list')

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
