from ..models import PostSpecificUser
from django.shortcuts import get_object_or_404
from django.db.models import Q  


def manage_post_specific_user_create(**kwargs):
    post_specific_user_data = PostSpecificUser.objects.create(
            created_by=kwargs['created_by'],
            post_id=kwargs['post_id'],
            specific_user_id=kwargs['specific_user_id'],
        )
    return post_specific_user_data
   