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
    full_name = models.CharField(max_length=512, default='', null=True, blank=True)
    picture = models.URLField(max_length=1200,null=True,blank=True)
    establishments_fav = models.ManyToManyField('establishment.Establishment', related_name="gas_favs", help_text="Estabelecimentos Favoritos Favoritos", blank=True)

    USERNAME_FIELD = 'username'


@receiver(post_save, sender=UserProfile)
def user_save_schedule(instance, **kwargs):
    if kwargs['created']:
        Token.objects.create(user=instance)


class PushToken(models.Model):
    key = models.CharField('Token Push', max_length=60)
    user = models.ForeignKey(UserProfile, null=False, blank=False, on_delete=models.CASCADE)
    is_mobile = models.BooleanField('E do App?', default=False)
    is_web = models.BooleanField('E do Admin Web?', default=False)
    is_active = models.BooleanField('Ativo?', default=True)

    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)