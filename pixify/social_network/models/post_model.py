from django.db import models
from ..constants import PostType, AccessLevel, PostContentType, SpecificUserTreatment

class Post(models.Model):
    posted_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, default=None, related_name='fk_post_posts_users_id')
    type = models.IntegerField(
        choices=[(type.value, type.name) for type in PostType],
        blank=False,
        default = PostType.NORMAL.value
    )
    content_type = models.IntegerField(
        choices=[(type.value, type.name) for type in PostContentType],
        blank=False,
        default= PostContentType.TEXT.value
    )
    media_url = models.URLField(max_length=200, blank=True) 
    title = models.CharField(max_length=50)
    description = models.TextField
    
    accessability = models.IntegerField(
        choices=[(level.value, level.name) for level in AccessLevel],
        blank= False,
        default = AccessLevel.PUBLIC.value
    )
    members = models.ManyToManyField(
        'User', through='PostSpecificUser', related_name='fk_members_chats_users'
    )
    treat_as = models.IntegerField(
        choices=[(type.value, type.name) for type in SpecificUserTreatment],
        blank=False,
        default= SpecificUserTreatment.INCLUDE.value
    )

    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_create_posts_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_update_posts_users_id')
    
    class Meta:
        db_table = 'posts'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"