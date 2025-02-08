from django.db import models
from django.contrib.postgres.fields import ArrayField
from social_network.constants.default_values import Role, UIMODES
from ..constants import Gender, RelationShipStatus
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # set role while creating user, default value is not working
    roles = ArrayField(
        models.IntegerField(
            choices=[(type.value, type.name) for type in Role],
            db_default=Role.END_USER.value,
            blank=True
        ),
        blank=True
    )
    address = models.CharField(blank=True, null=True, max_length=100)
    hobbies = ArrayField(models.CharField(max_length=50,blank=True, null=True), null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    profile_photo_url = models.URLField(max_length=200, null=True, blank=True)
    cover_photo_url = models.URLField(max_length=200, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.IntegerField(
        choices=[(gender.value, gender.name) for gender in Gender],
        blank=True,
        null=True
    )
    relationship_status = models.IntegerField(
        choices=[(status.value, status.name) for status in RelationShipStatus],
        blank=True,
        null=True
    )
    country = models.CharField(max_length=40, blank=True, db_default='INDIA')
    # timezone
    fcm_token = models.CharField(max_length=512, blank=True, null=True)
    ui_mode = models.IntegerField(
        choices=[(mode.value, mode.name) for mode in UIMODES],
        blank=True,
        db_default=UIMODES.LIGHT.value
    )

    is_active = models.BooleanField(db_default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_create_users_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name='fk_update_users_users_id')

    # fields required for abstract user
    groups = None
    user_permissions = None
    username = models.CharField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)
    is_staff = models.BooleanField(db_default=False, blank=True)  # To allow admin access
    is_superuser = models.BooleanField(db_default=False, blank=True)  # Superuser status


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # for web_cam_verification
    #  =models.ImageField(upload_to='verification_images/', null=True, blank=True)
    # is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
         return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"