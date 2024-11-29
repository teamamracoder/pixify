from ..models import User,Post,Comment
from ..packages.get_data import GetData
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



def manage_list_posts_filtered(search_query, sorting_order, sort_by, page_number):
     # get data
    data = (
        GetData(Post)
        .search(search_query,"posted_by","title","descriptions")
        .sort(sort_by, sorting_order)
        .paginate(limit=10, page=page_number)
        .execute()
    )
    # return data
    return data    

def get_comment_count_by_post(post_id):
    comment_count = Comment.objects.filter(post_id=post_id, reply_for__isnull=True, is_active=True).count()
    return comment_count


def manage_list_comments_filtered(post_id):
    return models.Comment.objects.filter(post_id=post_id, reply_for__isnull=True, is_active=True)



