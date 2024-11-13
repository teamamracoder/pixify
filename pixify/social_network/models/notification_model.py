from django.db import models

class Notification(models.Model):
    text = models.CharField(blank=True,null=True,max_length=50)
    media_url = models.URLField(max_length=200) 
    receiver_id = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='fk_receiver_notifications_users_id')
    is_read = models.BooleanField(db_default= False)
    
    is_active = models.BooleanField(db_default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, db_default=None, related_name='fk_create_notifications_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, db_default=None, related_name='fk_update_notifications_users_id')
  
    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
    






