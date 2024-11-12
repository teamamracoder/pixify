from django.db import models

class MessageReaction(models.Model):
    reacted_by=models.ForeignKey('User', on_delete=models.CASCADE,blank=False, related_name='fk_reacted_messagereactions_users_id')
    message_id=models.ForeignKey('Message', on_delete=models.CASCADE,blank=False, related_name='fk_reacted_messagereactions_messages_id')
    reaction_type=models.CharField(blank=False)
    
    is_active=models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by=models.ForeignKey('User', on_delete=models.CASCADE,blank=True, default=None,related_name='fk_created_messagereactions_users_id',null=True)
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True,default=None, related_name='fk_updated_messagereactions_users_id',null=True)
    
    class Meta:
        db_table = 'message_reactions'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
