from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Score, Tokens

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'score', 'tokens', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'score', 'tokens')
    ordering = ('-created_at',)


class TokensAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_tokens', 'claimed_tokens', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'claimed_token')
    ordering = ('-created_at',)

# Register the new UserAdmin
admin.site.register(Score, ScoreAdmin)
admin.site.register(Tokens, TokensAdmin)