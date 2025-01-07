from django.contrib import admin
from .models import Ad

class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'title', 'category', 'brand', 'price_original', 'price_discounted', 'currency','embeded_code', 'stock_status', 'created_at')
    list_filter = ('source', 'category', 'brand', 'stock_status')  # Add filters for easy navigation
    search_fields = ('title', 'product_id', 'category', 'brand')  # Enable search functionality
    ordering = ('-created_at',)  # Order by most recent ads first

# Register the Ad model with the custom admin configuration
admin.site.register(Ad, AdAdmin)
