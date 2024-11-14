from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime

from social_network.constants.default_values import Role
from ..constants import Gender, RelationShipStatus
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    first_name = models.CharField(max_length=50, default=None)
    middle_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    email = models.EmailField(unique=True)
    roles = ArrayField(
        models.IntegerField(choices=[(type.value, type.name) for type in Role], default=Role.END_USER),
        default=list
    )
    address = models.CharField(blank=True, null=True, max_length=100)
    hobbies = ArrayField(models.CharField(max_length=50,blank=True, default=None), default=list)
    bio = models.CharField(max_length=100, null=True)
    profile_photo_url = models.URLField(max_length=200, null=True)
    cover_photo_url = models.URLField(max_length=200, null=True)
    dob = models.DateField(blank=False,default=datetime.date(1950, 1, 1))
    gender = models.IntegerField(
        choices=[(gender.value, gender.name) for gender in Gender],
        blank=True,
        default=None
    )
    relationship_status = models.IntegerField(
        choices=[(status.value, status.name) for status in RelationShipStatus],
        blank=True,
        default=None
    )

    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='fk_create_users_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='fk_update_users_users_id')
    
    # fields required for abstract user
    groups = None
    user_permissions = None
    username = models.CharField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)  # To allow admin access
    is_superuser = models.BooleanField(default=False)  # Superuser status

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
    
    def __str__(self):
         return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"