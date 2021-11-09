from django.db import models

from establishment.models import Establishment
from user.models import UserProfile


class Events(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    establishment = models.ForeignKey(Establishment, related_name='events_establishment',on_delete=models.deletion.CASCADE)
    description = models.TextField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=50, blank=False, null=False)
    image_url = models.URLField(null=False, blank=False)

    class Meta:
        verbose_name = "Eventos"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return '{name} - {id}'.format(name=self.title, id=self.id)

class Banner(models.Model):
    image_url = models.URLField(null=False, blank=False)
    event = models.ForeignKey(Events, related_name='banners_events', null=False, blank=False, on_delete=models.deletion.CASCADE)
    class Meta:
        verbose_name = "Banner Eventos"
        verbose_name_plural = "Banner Eventos"

class Ticket(models.Model):
    code = models.CharField(max_length=9, null=False, blank=False)
    expiration_date = models.DateTimeField(null=False, blank=False)
    event = models.ForeignKey(Events, related_name='ticket_event',on_delete=models.deletion.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='ticket_user',
                                      on_delete=models.deletion.CASCADE)
