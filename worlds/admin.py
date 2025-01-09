from django.contrib import admin
from .models import World, Brand

class WorldsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    ordering = ('-created_at',)

class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_token_info', 'started_date', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

    def get_token_info(self, obj):
        return ", ".join([token_info.token_name for token_info in obj.tokenInfo.all()])
    get_token_info.short_description = 'Token Info'



# Register the new UserAdmin
admin.site.register(World, WorldsAdmin)
admin.site.register(Brand, BrandsAdmin)
