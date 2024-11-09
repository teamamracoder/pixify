from django.db import models

class MessageReadStatus(models.Model): 
    message_id = models.ForeignKey('Message', on_delete=models.CASCADE, blank=True, related_name='fk_message_msg_status_messages_id')
    read_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_readby_msg_status_users_id')
    read_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_create_msg_status_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_update_msg_status_users_id')

    class Meta:
        db_table = 'message_read_status'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
