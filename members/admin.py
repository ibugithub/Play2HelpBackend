from django.contrib import admin
from .models import Members


class MembersAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'get_brands', 'role', 'joined_date', 'earned_tokens', 'earned_dollars', 'ownership', 'created_at', 'updated_at') 
    list_filter = ('name', 'role', 'created_at')
    search_fields = ('name', 'role') 
    ordering = ('-created_at',)

    def get_brands(self, obj):
        return ", ".join([brand.name for brand in obj.brands.all()])
    get_brands.short_description = 'Brands'


# Register the new UserAdmin
admin.site.register(Members, MembersAdmin)

