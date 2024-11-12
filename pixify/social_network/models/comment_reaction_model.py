from django.db import models

class CommentReaction(models.Model):                                                    
    reacted_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True,null=True, default=None, related_name='fk_reacted_comment_reactions_users_id')
    comment_id = models.ForeignKey('Comment',on_delete=models.CASCADE,blank=True,null=True, related_name='fk_comment_comment_reactions_users_id')
    reation_type = models.CharField(blank=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True,default=None, related_name='fk_create_comment_reactions_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True,null=True, default=None, related_name='fk_update_comment_reactions_users_id')

    class Meta:
        db_table = 'comment_reactions'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"






