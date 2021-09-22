from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# The username will be a hashcode.
class UserProfile(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_facebook_user = models.BooleanField(default=False)
    facebook_id = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=512, default='')
    picture = models.URLField(null=True,blank=True)
    USERNAME_FIELD = 'username'


@receiver(post_save, sender=UserProfile)
def user_save_schedule(instance, **kwargs):
    if kwargs['created']:
        Token.objects.create(user=instance)