from .. import models
from django.shortcuts import get_object_or_404

def list_posts(): 
    return models.Post.objects.all()

def create_post(**kwargs):
    print(kwargs['posted_by'])
    print(kwargs['type'])
    print(kwargs['content_type'])
    print(kwargs['media_url'])
    post = models.Post.objects.create(
            posted_by=kwargs['posted_by'],
            type=kwargs['type'],
            content_type=kwargs['content_type'],
            media_url=kwargs.get('media_url'),
            title=kwargs['title'],
            description=kwargs['description'],
            accessability=kwargs['accessability'],
            members  = kwargs['members'],
            treat_as = kwargs['treat_as'],
            is_active=kwargs.get('is_active', True) 
        )
    post.save()
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