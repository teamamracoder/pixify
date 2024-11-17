from django.db import models
from ..constants import MASTERTYPE

class MasterList(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    value = models.CharField(max_length=100)
    type = models.IntegerField(
        choices=[(type.value, type.name) for type in MASTERTYPE]
    )
    
    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_create_master_list_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_master_list_users_id')
  
    class Meta:
        db_table = 'master_lists'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"