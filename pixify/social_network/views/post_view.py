from django.shortcuts import render, redirect
from django.views import View
from .. import services
from ..constants import PostType,Gender,PostContentType,AccessLevel,SpecificUserTreatment


class PostListView(View):
    def get(self, request):
        posts = services.post_service.list_posts()
        return render(request, 'adminuser/post/list.html', {'posts': posts})

class PostCreateView(View):
    def get(self, request):
        choices_file = [{posttype.value: posttype.name} for posttype in PostType]
        #choices_relationship_status = [{status.name: status.value} for status in RelationShipStatus]
        # return render(request,'adminuser/post/create.html',{"choices_file":choices_file})
        return render(request,'adminuser/post/create.html',{"choices_file":choices_file,"PostType":PostType})


    def post(self, request):
        print(request.POST)
        print(request.POST["description"])
        print(type(request.POST["description"]))
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
