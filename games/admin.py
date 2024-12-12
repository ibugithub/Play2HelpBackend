from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Score, Tokens, TokenInfo, MerkelDatastructure

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'score', 'tokens', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'score', 'tokens')
    ordering = ('-created_at',)


class TokensAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_tokens', 'claimed_tokens', 'last_claimed_date', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'claimed_token')
    ordering = ('-created_at',)

class TokensInfoAdmin(admin.ModelAdmin):
    list_display = ('token_name', 'token_address', 'created_at', 'updated_at')
    list_filter = ('token_name', 'created_at')
    search_fields = ('token_address', 'token_name')
    ordering = ('-created_at',)
    
    
class MerkelDataStructureAdmin(admin.ModelAdmin):
    list_display = ('serialized_leaves', 'modified_date', 'created_at', 'updated_at')
    list_filter = ('serialized_leaves', 'created_at')
    search_fields = ('modified_date',)
    ordering = ('-created_at',)

# Register the new UserAdmin
admin.site.register(Score, ScoreAdmin)
admin.site.register(Tokens, TokensAdmin)
admin.site.register(TokenInfo, TokensInfoAdmin)
admin.site.register(MerkelDatastructure, MerkelDataStructureAdmin)