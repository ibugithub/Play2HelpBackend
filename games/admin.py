from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Score

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'score')
    ordering = ('-created_at',)

# Register the new UserAdmin
admin.site.register(Score, ScoreAdmin)