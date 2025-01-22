from ..models import Post,User,Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import User
from .. import models





def user_comments_create(commentstext,post_id,user_id,):
    return Comment.objects.create(comment=commentstext,created_by_id=user_id,comment_by_id=user_id,post_id_id=post_id)



def get_count_comment(postid):
    return Comment.objects.filter(post_id_id=postid).count()


def comment_list(post_id):
    return models.Comment.objects.filter(post_id=post_id).order_by('created_at').values()



def comments_filtered(post_id):
    return  Comment.objects.filter(post_id_id=post_id)


def get_post(post_id):
    return Post.objects.filter(id=post_id)


def get_user(user_id):
    return User.objects.filter(id=user_id)


