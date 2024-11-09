from django.db import models
from django.core.exceptions import ValidationError

class Follower(models.Model):
    # virtual field
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_follower_followers_users_id')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_following_followers_users_id')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='follow_pair')
        ]
    def clean(self):
        if self.follower == self.following:
            raise ValidationError("A user cannot follow themselves.")
        
    is_active  = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)        
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_create_followers_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_update_followers_users_id')
    
    class Meta:
         db_table = 'followers'

    def __str__(self):
         return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
