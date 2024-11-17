from django.db import models

class PostReaction(models.Model):
    reacted_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, related_name='fk_reacted_post_reactions_users_id')
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, blank=False, related_name='fk_post_post_reaction_post_id')
    # reaction_type = models.CharField(blank=False)
    
    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_post_reactions_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_post_reactions_users_id')
    
    class Meta:
        db_table = 'post_reactions'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"






