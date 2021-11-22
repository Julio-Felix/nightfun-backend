from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

class UserAdmin(BaseUserAdmin):
    search_fields = ['username', 'first_name', 'last_name',]
    list_display = ('username', 'first_name', 'last_name',)
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        ('Usuario', {'fields': ('username', 'password')}),
        ('Info', {'fields': (
            'first_name',
            'last_name',
            'email',
        )}),
        ('Permissoes', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
    )


admin.site.register(UserProfile, UserAdmin)

# Register your models here.
