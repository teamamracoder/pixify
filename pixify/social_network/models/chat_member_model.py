from django.db import models
from django.utils import timezone

class ChatMember(models.Model):
    chat_id = models.ForeignKey('Chat', on_delete=models.CASCADE, default=None)
    member_id = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    joined_at = models.DateTimeField(default=timezone.now)
    
    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_create_chatmembers_users_id' )
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_update_chatmembers_users_id')
    
    class Meta:
        db_table = 'chat_members'
        constraints = [
            models.UniqueConstraint(fields=['chat_id', 'member_id'], name='chat_member_pair')
        ]
        
    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
    