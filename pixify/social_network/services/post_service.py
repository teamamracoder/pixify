from ..models import User,Post,Comment
from django.shortcuts import get_object_or_404
from social_network.packages.get_data import GetData

from .. import models

def manage_list_posts():
    return Post.objects.all()

def manage_get_post(post_id):
    return get_object_or_404(Post, id=post_id)

def manage_get_user(posted_by):
    return get_object_or_404(User, id=posted_by)

def manage_update_post(post, title, description):
    post.title = title
    post.description = description
    post.save()
    return post

def manage_delete_post(post):
    post.delete()



# new added by sujit
def manage_list_posts(sort_by = 'title'): 
    return Post.objects.all().order_by(sort_by)

def manage_create_post(**kwargs):
    post = Post.objects.create( # creating a new post object
            posted_by=kwargs['posted_by'],
            created_by=kwargs['created_by'],
            title=kwargs['title'],
            description=kwargs['description'],
        )
    return post

def manage_list_posts_filtered(search_query,sort_by='posted_by'):
    if search_query:
        # Use Q objects to filter by posted_by, title, or descriptions
        return Post.objects.filter(
            Q(posted_by__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by(sort_by)
    return Post.objects.all().order_by(sort_by)    


