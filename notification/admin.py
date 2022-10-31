from django.contrib import admin
from django.contrib import messages

from notification.models import NotificationCenter
# from notification.utils import send_notification, NotificationFailed, NOTIFICATION_BY_DJANGO

from django.utils.translation import ugettext_lazy as _


class NotificationCenterAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'createAt']
    search_fields = ['title']
    readonly_fields = ('user', 'request_json', 'createAt', 'updateAt')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'message'),
        }),
    )
    fieldsets = (
        (_('Notificacao'), {'fields': ('title', 'message', 'user')}),
        (_('Important dates'), {'fields': ('createAt', 'updateAt')}),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
        # push_tokens = PushToken.objects.filter(is_active=True)
        # ids_push = list(push_tokens.values_list('key', flat=True))
        # user_ids = list(push_tokens.values_list('user_id', flat=True))
        #
        # try:
        #     status_not = send_notification(ids_push, obj.title, obj.message, NOTIFICATION_BY_DJANGO, user_ids, request.user.id, None, obj.id)
        #     messages.add_message(request, messages.SUCCESS, _(status_not))
        # except NotificationFailed as err:
        #     # pass
        #     messages.add_message(request, messages.ERROR, _('Notificacao Falhou Completamente, '
        #                                                     'Por Favor Entrar em Contato com Suporte - '
        #                                                     'Failed Due to ' + str(err)))

admin.site.register(NotificationCenter, NotificationCenterAdmin)

