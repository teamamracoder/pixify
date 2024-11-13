from django.db import models
from django.utils import timezone

class MessageMention(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    mentioned_at = models.DateTimeField(db_default=timezone.now)

    is_active = models.BooleanField(db_default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, db_default=None, related_name='fk_create_messagementions_users_id' )
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, db_default=None, related_name='fk_update_messagementions_users_id')

    class Meta:
        db_table = 'message_mentions'
        constraints = [
            models.UniqueConstraint(fields=['message', 'user'], name='messag_mention_pair')
        ]

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"