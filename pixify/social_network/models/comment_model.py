from django.db import models

class Comment(models.Model):
    comment_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_comment_comments_users_id')
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='fk_post_comments_post_id')
    comment = models.CharField(max_length=100)
    reply_for = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_reply_comments_comment_id')

    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_comments_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_comments_users_id')
    
    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"