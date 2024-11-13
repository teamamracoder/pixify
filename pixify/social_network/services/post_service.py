from .. import models
from django.shortcuts import get_object_or_404

def list_posts(): 
    return models.Post.objects.all()

def create_post(**kwargs):
    post = models.Post.objects.create(
            posted_by=kwargs['posted_by'],
            type=kwargs['type'],
            content_type=kwargs['content_type'],
            media_url=kwargs.get('media_url'),
            title=kwargs['title'],
            # description=kwargs['description'],
            accessability=kwargs['accessability'],
            is_active=kwargs.get('is_active', True) 
        )
    return post


def get_post(post_id):
    return get_object_or_404(models.Post, id=post_id)

def update_post(post, title, description):
    post.title = title
    post.description = description
    post.save()
    return post

def delete_post(post):
    post.delete()

########################################################################
# def create_post(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
        
#         # Retrieve the User instance and create the Post object
#         user_instance = User.objects.get(id=1)  # Replace 1 with the actual user ID you need
#         post_instance = Post(title=title, content=content, posted_by=user_instance)
#         post_instance.save()

#         return redirect('some_view_name')  # Redirect after saving the post
    
#     return render(request, 'adminuser/post/create.html')  # Render your form template here
