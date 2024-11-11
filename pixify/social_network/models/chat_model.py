from django.db import models
from ..constants import ChatType

class Chat(models.Model):
    title = models.CharField(null = True, blank = True)
    type = models.IntegerField(
        choices=[(type.value, type.name) for type in ChatType],
        blank=False,
        default=ChatType.PERSONAL.value
    )
    members = models.ManyToManyField(
        'User', through='ChatMember', through_fields=('chat_id','member_id'), related_name='fk_members_chats_users'
    )
    chat_cover = models.URLField(max_length=400, blank=True)
    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_create_chats_users_id' )
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, default=None, related_name='fk_update_chats_users_id')
    
    class Meta:
        db_table = 'chats'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
    




    