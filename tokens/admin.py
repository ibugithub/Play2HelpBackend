from django.contrib import admin
from .models import TokenInfo, MerkelDatastructure, TokenPeriod



class TokensInfoAdmin(admin.ModelAdmin):
    list_display = ('token_name', 'solana_contract_address', 'bnb_contract_address', 'total_value', 'total_tokens', 'token_prices', 'created_at', 'updated_at')
    list_filter = ('token_name', 'created_at')
    search_fields = ('token_address', 'token_name')
    ordering = ('-created_at',)

class TokenPeriodAdmin(admin.ModelAdmin):
    list_display = ('tokenInfo', 'token_count_date', 'token_duration')
    list_filter = ('tokenInfo', 'token_count_date')
    search_fields = ('tokenInfo', 'token_count_date')
    ordering = ('-token_count_date',)
    
class MerkelDataStructureAdmin(admin.ModelAdmin):
    list_display = ('serialized_leaves', 'modified_date', 'created_at', 'updated_at')
    list_filter = ('serialized_leaves', 'created_at')
    search_fields = ('modified_date',)
    ordering = ('-created_at',)
    

# Register the new UserAdmin
admin.site.register(TokenInfo, TokensInfoAdmin)
admin.site.register(MerkelDatastructure, MerkelDataStructureAdmin)
admin.site.register(TokenPeriod, TokenPeriodAdmin)
