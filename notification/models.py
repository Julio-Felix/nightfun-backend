from django.db import models

from establishment.models import Establishment
from user.models import UserProfile
from django.utils.translation import ugettext_lazy as _


class NotificationCenter(models.Model):
    user = models.ForeignKey(UserProfile, related_name='notificationcenter_user', null=False, blank=False,
                             on_delete=models.CASCADE)
    establishment = models.ForeignKey(Establishment, related_name='notificationcenter_establishment', on_delete=models.CASCADE)
    title = models.CharField(_("Titulo"), max_length=45, null=False, blank=False)
    message = models.CharField(_('Mensagem'), max_length=50, null=False, blank=False)
    request_json = models.TextField(_('JSON da Request'), blank=True, null=True)

    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name + ' - ' + self.message

    class Meta:
        verbose_name = _("Central de Notificacoes")
        verbose_name_plural = _("Central de Notificacoes")