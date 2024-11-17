from django.db import models

class Message(models.Model):
    text=models.CharField(max_length=200, blank=True, null=True)
    media_url= models.CharField(max_length=200, blank=True, null=True)
    sender_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_sender_messages_users_id')
    chat_id= models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='fk_chat_messages_chats_id')
    reply_for_message_id=models.ForeignKey('Message', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_reply_messages_messages_id')
    send_at=models.DateTimeField(auto_now_add=True, blank=True)
    reply_for_everyone = models.BooleanField(db_default=True, blank=True)
    mentions = models.ManyToManyField(
        'User', through='MessageMention', through_fields=('message','user'), related_name='fk_mentions_messages_users'
    )
    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_messages_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_messages_users_id')
    
    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"