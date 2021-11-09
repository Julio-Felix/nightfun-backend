from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from events.models import Events, Banner, Ticket

from django.contrib.admin.helpers import ActionForm
from django import forms
from django.contrib import messages
import datetime
from django.utils import timezone

class XForm(ActionForm):
    Cupom = forms.CharField(label="Cupom",required=False)


class EventsAdmin(admin.ModelAdmin):
    action_form = XForm
    actions = ['validate_cupom']
    def get_queryset(self, request):
        qs = super(EventsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(establishment__operators=request.user)

    def validate_cupom(self, request, queryset):
        print(request.POST['Cupom'])
        if len(queryset) > 1:
            self.message_user(request, "Por Favor Selecione Apenas um Estabelecimento", level=messages.WARNING)
        else:
            obj = queryset[0]
            now = timezone.now()
            try:
                ticket = Ticket.objects.get(code=request.POST['Cupom'], event=obj)
                if ticket:
                    if ticket.expiration_date >= now:
                        self.message_user(request, "Cupom Validado e Correto", level=messages.SUCCESS)
                    else:
                        self.message_user(request, "Cupom Validado, Porem Expirado", level=messages.WARNING)
                else:
                    self.message_user(request, "Cupom Invalido", level=messages.ERROR)
            except ObjectDoesNotExist:
                self.message_user(request, "Cupom Invalido", level=messages.ERROR)

    validate_cupom.short_description = "Validar Cupom de Estabelecimento"


admin.site.register(Events, EventsAdmin)
admin.site.register(Banner)