from ..models import Post,User,Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import User
from .. import models





def user_comments_create(commentstext,post_id,user_id,):
    return Comment.objects.create(comment=commentstext,created_by_id=user_id,comment_by_id=user_id,post_id_id=post_id)



def get_count_comment(postid):
    return Comment.objects.filter(post_id_id=postid).count()


# def comment_list(post_id):
#     return models.Comment.objects.filter(post_id=post_id).order_by('created_at').values()

def comment_list(post_id):
    comments = Comment.objects.filter(post_id=post_id).select_related('comment_by')
    return list(comments.values('id', 'comment', 'created_at', 
                                'comment_by__first_name', 'comment_by__last_name','reply_for_id'))

def comments_filtered(post_id):
    return  Comment.objects.filter(post_id_id=post_id)


def get_post(post_id):
    return Post.objects.filter(id=post_id)


def get_user(user_id):
    return User.objects.filter(id=user_id)

def get_comment_by(comment_by_id):
    return User.objects.filter(id=comment_by_id)



def user_reply_create(reply_text, post_id, user_id, comment_id):
    return Comment.objects.create(comment=reply_text,created_by_id=user_id,comment_by_id=user_id,post_id_id=post_id,reply_for_id=comment_id)


def reply_list(comment_id):
     return Comment.objects.filter(reply_for_id=comment_id)


def comment_count(post_id):
     return Comment.objects.filter(post_id_id=post_id, is_active=True).count()