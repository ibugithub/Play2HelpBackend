from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Score, TokenInfo, MerkelDatastructure, Game, Brands, Members, TotalScore

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'score', 'tokens', 'claimed_tokens', 'last_claimed_date', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'score', 'tokens')
    ordering = ('-created_at',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'tokenInfo', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    ordering = ('-created_at',)

class TokensAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_tokens', 'claimed_tokens', 'last_claimed_date', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'claimed_token')
    ordering = ('-created_at',)

class TokensInfoAdmin(admin.ModelAdmin):
    list_display = ('token_name', 'solana_contract_address', 'bnb_contract_address', 'created_at', 'updated_at')
    list_filter = ('token_name', 'created_at')
    search_fields = ('token_address', 'token_name')
    ordering = ('-created_at',)
    
class MerkelDataStructureAdmin(admin.ModelAdmin):
    list_display = ('serialized_leaves', 'modified_date', 'created_at', 'updated_at')
    list_filter = ('serialized_leaves', 'created_at')
    search_fields = ('modified_date',)
    ordering = ('-created_at',)
    
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('name', 'started_date', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

class MembersAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'get_brands', 'role', 'joined_date', 'created_at', 'updated_at') 
    list_filter = ('name', 'role', 'created_at')
    search_fields = ('name', 'role') 
    ordering = ('-created_at',)

    def get_brands(self, obj):
        return ", ".join([brand.name for brand in obj.brands.all()])
    get_brands.short_description = 'Brands' 

class TotalScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'total_tokens', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__email', 'total_score')
    ordering = ('-created_at',)


# Register the new UserAdmin
admin.site.register(Score, ScoreAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(TokenInfo, TokensInfoAdmin)
admin.site.register(MerkelDatastructure, MerkelDataStructureAdmin)
admin.site.register(Brands, BrandsAdmin)
admin.site.register(Members, MembersAdmin)
admin.site.register(TotalScore, TotalScoreAdmin)