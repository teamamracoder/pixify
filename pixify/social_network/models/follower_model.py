from django.db import models

class Follower(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_follower_followers_users_id',null=True, blank=1)
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_following_followers_users_id', null=True, blank=1)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_followers_users_id', null=True)
    is_active  = models.BooleanField(db_default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)        
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, db_default=None, related_name='fk_create_followers_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, db_default=None, related_name='fk_update_followers_users_id')
    
    class Meta:
        db_table = 'followers'
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='follow_pair'),
            models.CheckConstraint(check=~models.Q(follower=models.F('following')), name='follower_not_equal_to_following')
        ]

    def __str__(self):
         return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
