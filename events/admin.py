from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from events.models import Events, Banner, Ticket

from django.contrib.admin.helpers import ActionForm
from django import forms
from django.contrib import messages
import datetime
from django.utils import timezone

from user.models import PushToken


class XForm(ActionForm):
    Cupom = forms.CharField(label="Cupom",required=False)
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        raise

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        PushToken.objects.filter(token=token).update(active=False)
    except PushTicketError as exc:
        # Encountered some other per-notification error.
        raise

class EventsAdmin(admin.ModelAdmin):
    action_form = XForm
    actions = ['validate_cupom']
    def get_queryset(self, request):
        qs = super(EventsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(establishment__operators=request.user)

    def save_model(self, request, obj, form, change):
        # obj.user = request.user
        super().save_model(request, obj, form, change)
        users = obj.establishment.gas_favs.all()
        tokens = PushToken.objects.filter(user__in=users)
        for token in tokens:
            send_push_message(token.key, "Novo Evento do seu Estabelecimento Favorito")


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