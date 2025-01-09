from django.contrib import admin
from .models import Score, Game, TotalScore

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'tokenInfo', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    ordering = ('-created_at',)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'score', 'tokens', 'claimed_tokens', 'last_claimed_date', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'score', 'tokens')
    ordering = ('-created_at',)

class TotalScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'total_tokens', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'total_score')
    ordering = ('-created_at',)


# Register the new UserAdmin
admin.site.register(Score, ScoreAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(TotalScore, TotalScoreAdmin)
