from ..models import Comment
from ..packages.get_data import GetData
from .. import models
from django.shortcuts import get_object_or_404


def manage_create_comment(**kwargs):
    comment = models.Comment.objects.create(      
            comment=kwargs['comment'],           
            post_id=kwargs['post_id'],
            comment_by=kwargs['comment_by'],
            created_by=kwargs['created_by']             
        )
    
    return comment




def manage_list_comments_filtered(post_id):
    return models.Comment.objects.filter(post_id=post_id, reply_for__isnull=True, is_active=True)


def manage_list_comments():
    return models.Comment.objects.all()

def manage_get_comment(comment_id):
    return get_object_or_404(models.Comment, id=comment_id)
 