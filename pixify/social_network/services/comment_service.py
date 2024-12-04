from ..models import Post,User,Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import User
from .. import models





def user_comments_create(commentstext,user_id,post_id):
    return Comment.objects.create(comment=commentstext,created_by_id=user_id,comment_by_id=user_id,post_id_id=post_id)
# ,post_id_id=post_id


def get_count_comment(post_id):
    return Comment.objects.filter(post_id_id=post_id).count()


def comment_list(post_id):
    return models.Comment.objects.filter(post_id=post_id).order_by('created_at').values()

# def comment_list(post_id):
#      return models.Comment.objects.all().order_by('created_at').values()
     

def comments_filtered(post_id):
    return  Comment.objects.filter(post_id_id=post_id)


def get_post(post_id):
    return get_object_or_404(Post, id=post_id)

