from django.db import models
# badhan
# from social_network.models import Follower


class Follower(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_followers_users_id')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_follower_followers_users_id', null=True, blank=True)
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_following_followers_users_id', null=True, blank=True)
    is_active  = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)    
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_followers_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_followers_users_id')
    
    class Meta:
        db_table = 'followers'
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='follow_pair'),
            models.CheckConstraint(check=~models.Q(follower=models.F('following')), name='follower_not_equal_to_following')
        ]

    def __str__(self):
         return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
    
