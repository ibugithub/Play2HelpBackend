from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'user_Image_url', 'is_verified', 'is_admin', 'wallet_address')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Basic', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'wallet_address')}),
        ('Permissions', {'fields': ('is_admin', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()

# Register the new UserAdmin
admin.site.register(User, UserAdmin)