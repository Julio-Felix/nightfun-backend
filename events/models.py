from django.db import models

from establishment.models import Establishment


class Events(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    establishment = models.ForeignKey(Establishment, related_name='events_establishment',on_delete=models.deletion.CASCADE)
    description = models.TextField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=50, blank=False, null=False)
    image_url = models.URLField(null=False, blank=False)


class Banner(models.Model):
    image_url = models.URLField(null=False, blank=False)
    event = models.ForeignKey(Events, null=False, blank=False,on_delete=models.deletion.CASCADE)
