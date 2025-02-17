from ..models.user_model import User
from . import GetData
from ..models import Post,Comment,PostReaction,PostReaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..constants.default_values import PostType

from ..import models


def delete_post(post):
    post.delete()

# priya
def user_post(post_Title,media_urls,user_id):
          return Post.objects.create(title=post_Title,media_url=media_urls,created_by_id=user_id,posted_by_id=user_id)

# priya
def Postlist_posts():
    return Post.objects.filter(type=PostType.NORMAL.value).order_by('-created_at')

def get_post(post_id):
     return get_object_or_404(Post, id=post_id)

def get_comment_count_by_post(post_id):
    comment_count = Comment.objects.filter(post_id=post_id, reply_for__isnull=True, is_active=True).count()
    return comment_count


def get_post(post_id):
    return Post.objects.filter(id=post_id)


# update post
def update_post(user_id,post_id,post_titile):
    post = Post.objects.get(id=post_id)
    post.title = post_titile
    post.updated_by=user_id
    post.save()
    # return post

# comment
def reaction_name(post_id):
   return PostReaction.objects.filter( post_id_id=post_id, is_active=True).first()