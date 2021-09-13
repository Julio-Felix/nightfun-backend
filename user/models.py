from django.contrib.auth.models import AbstractUser
from django.db import models


# The username will be a hashcode.
class UserProfile(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_facebook_user = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=512, default='')
    picture = models.URLField(null=True,blank=True)
    USERNAME_FIELD = 'username'
