from django.db import models
from ..constants import ChatType
from django.db.models import Q

class Chat(models.Model):
    title = models.CharField(null=True, blank=True)
    type = models.IntegerField(
        choices=[(type.value, type.name) for type in ChatType],
        blank=False,
        db_default=ChatType.PERSONAL.value
    )
    members = models.ManyToManyField(
        'User', 
        through='ChatMember', 
        through_fields=('chat_id','member_id'),
        related_name='fk_members_chats_users'
    )
    chat_cover = models.URLField(max_length=400, blank=True, null=True)
    chat_bio = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_chats_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_chats_users_id')
    
    class Meta:
        db_table = 'chats'
        constraints = [
            # For personal chats, chat_bio must be null or empty.
            models.CheckConstraint(
                check=(~Q(type=ChatType.PERSONAL.value)) | Q(chat_bio__isnull=True) | Q(chat_bio=''),
                name='chat_bio_only_for_group'
            ),
        ]

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
