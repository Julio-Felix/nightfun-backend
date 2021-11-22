from django.contrib import admin
from .models import *
class EstablishmentAdmin(admin.ModelAdmin):
    filter_horizontal = ('operators',)
    def get_queryset(self, request):
        qs = super(EstablishmentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(operators=request.user)

admin.site.register(Address)
admin.site.register(Establishment, EstablishmentAdmin)
admin.site.register(Schedules)
admin.site.register(Comments)
# Register your models here.
