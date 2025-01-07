from django.contrib import admin
from .models import Ad, World


class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'title', 'category', 'brand', 'price_original', 'price_discounted', 'currency','embeded_code', 'stock_status', 'created_at')
    list_filter = ('source', 'category', 'brand', 'stock_status')  # Add filters for easy navigation
    search_fields = ('title', 'product_id', 'category', 'brand')  # Enable search functionality
    ordering = ('-created_at',)  # Order by most recent ads first

# Register the Ad model with the custom admin configuration
admin.site.register(Ad, AdAdmin)


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    list_display = ('name', 'ad_categories')  # Fields to display in the admin list view
    search_fields = ('name',)  # Add a search bar for the name field
    list_filter = ('ad_categories',)  # Add a filter for ad categories