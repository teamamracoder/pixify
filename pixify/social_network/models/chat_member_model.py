from django.db import models

class ChatMember(models.Model):
    chat_id = models.ForeignKey('Chat', on_delete=models.CASCADE)
    member_id = models.ForeignKey('User', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_chatmembers_users_id' )
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_chatmembers_users_id')
    
    class Meta:
        db_table = 'chat_members'
        constraints = [
            models.UniqueConstraint(fields=['chat_id', 'member_id'], name='chat_member_pair')
        ]
        
    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
    