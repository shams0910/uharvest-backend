from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Account


class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),

        (_('Personal info'), {'fields': ('first_name', 'last_name', "role")}),

        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),

        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ('first_name',)

    list_display = ('id', 'phone', 'first_name', 'last_name', 'role')


# Register your models here.

admin.site.register(Account, CustomUserAdmin)
