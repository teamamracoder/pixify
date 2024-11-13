from .. import models
from django.shortcuts import get_object_or_404

def list_posts(): 
    return models.Post.objects.all()

def create_post(posted_by,content_type,accessability,media_url,members,treat_as):
    # print("These are valurs" + first_name,last_name,email)
    return models.Post.objects.create(posted_by=posted_by, content_type=content_type,accessability=accessability,media_url=media_url,members=members,treat_as=treat_as)

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
