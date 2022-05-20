from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import NextofKin, Security, User, Profile
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'email', 'password', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'username')
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Security)
admin.site.register(NextofKin)
admin.site.register(Profile)