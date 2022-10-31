import datetime
from datetime import timezone

from django.db import models

from user.models import UserProfile

SUNDAY = 1
MONDAY = 2
TUESDAY = 3
WEDNESDAY = 4
THURSDAY = 5
FRIDAY = 6
SATURDAY = 7
WEEK_DAYS = (
    (SUNDAY, 'Domingo'),
    (MONDAY, 'Segunda-feira'),
    (TUESDAY, 'Terça-feira'),
    (WEDNESDAY, 'Quarta-feira'),
    (THURSDAY, 'Quinta-feira'),
    (FRIDAY, 'Sexta-feira'),
    (SATURDAY, 'Sábado'),
)
SHIFT_CLOSED = 0
SHIFT_1 = 1
SHIFT_24_HOURS = 2

SHIFTS = ((SHIFT_CLOSED, 'Fechado'),
          (SHIFT_1, 'Período 1'),
          (SHIFT_24_HOURS, '24 horas'),)


# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=20, null=False, blank=False)
    neighborhood = models.CharField(max_length=20, null=False, blank=False)
    number = models.IntegerField()
    city = models.CharField(max_length=20, null=False, blank=False)
    state = models.CharField(max_length=2, null=False, blank=False)
    class Meta:
        verbose_name = "Endereços"
        verbose_name_plural = "Endereços"

class Establishment(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(max_length=200, blank=False, null=False)
    lat = models.FloatField()
    long = models.FloatField()
    email = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    address = models.ForeignKey(Address, null=False, blank=False, on_delete=models.deletion.CASCADE)
    cupom = models.BooleanField(default=True)
    operators = models.ManyToManyField(UserProfile, blank=True,related_name='operators_establishment')
    logo = models.URLField(max_length=1200,null=True,blank=True)


    class Meta:
        verbose_name = "Estabelecimento"
        verbose_name_plural = "Estabelecimentos"

    def __str__(self):
        return '{name} - {id}'.format(name=self.name,id=self.id)

class Schedules(models.Model):
    establishment = models.ForeignKey(Establishment, related_name='sch_establishment',on_delete=models.deletion.CASCADE)
    week_days = models.IntegerField(choices=WEEK_DAYS)
    sch_shift = models.IntegerField(choices=SHIFTS)
    sch_begin_shift = models.TimeField(null=False, blank=False)
    sch_end_shift = models.TimeField(null=False, blank=False)
    class Meta:
        verbose_name = "Horarios"
        verbose_name_plural = "Horarios"



class Comments(models.Model):
    text = models.TextField(null=True, blank=True)
    linked = models.BooleanField()
    establishment = models.ForeignKey(Establishment, related_name='comment_establishment',on_delete=models.deletion.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='comment_user', on_delete=models.deletion.CASCADE)
    createAt = models.DateTimeField(default=datetime.datetime.now)
    updateAt = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = "Comentários"
        verbose_name_plural = "Comentários"
        ordering = ['-createAt']