from django.db import models
from ..constants import PostType, AccessLevel, PostContentType, SpecificUserTreatment
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    posted_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_post_posts_users_id')
    type = models.IntegerField(
        choices=[(type.value, type.name) for type in PostType],
        blank=True,
        db_default= PostType.NORMAL.value
    )
    content_type = models.IntegerField(
        choices=[(type.value, type.name) for type in PostContentType],
        blank=True,
        db_default= PostContentType.TEXT.value
    )
    media_url = ArrayField(
        models.URLField(max_length=200, blank=True, null=True),
        blank=True,
        null=True
    )
        
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    accessability = models.IntegerField(
        choices=[(level.value, level.name) for level in AccessLevel],
        blank= True,
        db_default= AccessLevel.PUBLIC.value
    )
    # relationship
    members = models.ManyToManyField(
        'User', through='PostSpecificUser', through_fields=('post_id', 'specific_user_id'), related_name='fk_members_post_users'
    )
    
    tags = models.ManyToManyField(
        'User', through='PostUserTags', through_fields=('post', 'user'), related_name='fk_tags_post_users'
    )
    
    treat_as = models.IntegerField(
        choices=[(type.value, type.name) for type in SpecificUserTreatment],
        blank=True,
        db_default= SpecificUserTreatment.INCLUDE.value
    )

    is_active = models.BooleanField(db_default=True,blank=True)
    # created_at and updated_at will be automatically added into db table and those are note editable
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    # created_by is mendatory in all tables except 'users' table
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_posts_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_posts_users_id')
    
    class Meta:
        db_table = 'posts'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"