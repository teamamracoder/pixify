from django.db import models

class PostSpecificUser(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, blank=False, related_name='fk_post_post_specifc_users_post_id')
    specific_user_id = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, db_default=None, related_name='fk_post_post_specifc_users_user_id')    
    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_post_specific_users_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_post_specific_users_users_id')
  
    class Meta:
        db_table = 'post_specific_users'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"