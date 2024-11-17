from django.db import models

class MessageReaction(models.Model):
    reacted_by=models.ForeignKey('User', on_delete=models.CASCADE,related_name='fk_reacted_messagereactions_users_id')
    message_id=models.ForeignKey('Message', on_delete=models.CASCADE,related_name='fk_reacted_messagereactions_messages_id')
    # reaction_type=models.CharField()
    
    is_active=models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by=models.ForeignKey('User', on_delete=models.CASCADE,blank=True, related_name='fk_create_messagereactions_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_messagereactions_users_id')
    
    class Meta:
        db_table = 'message_reactions'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
