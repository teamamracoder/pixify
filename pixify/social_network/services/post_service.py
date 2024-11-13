# from .. import models
# from django.shortcuts import get_object_or_404

# def list_posts():
#     return models.Post.objects.all()

# def create_post(title, description):
#     return models.Post.objects.create(title=title, description=description)

# def get_post(post_id):
#     return get_object_or_404(models.Post, id=post_id)

# def update_post(post, title, description):
#     post.title = title
#     post.description = description
#     post.save()
#     return post

# def delete_post(post):
#     post.delete()

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
