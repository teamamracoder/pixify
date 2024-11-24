from tokenize import Comment
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







# def manage_list_comments_filtered(search_query, sorting_order, sort_by, page_number):
#     # get data
#     data = (
#         GetData(Comment)
#         .search(search_query,"comment","post_id")
#         .sort(sort_by, sorting_order)
#         .paginate(limit=3, page=page_number)
#         .execute()
#     )
#     return data

def manage_list_comments_filtered():
    return models.Comment.objects.all()


def manage_get_comment(comment_id):
    return get_object_or_404(models.Comment, id=comment_id)



def get_comment(comment_id):
    return get_object_or_404(Comment, id=comment_id)