from django.db import models
from django.utils.timezone import now

class Ad(models.Model):
    source = models.CharField(max_length=50)  # e.g., "Amazon", "Alibaba"
    product_id = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price_original = models.DecimalField(max_digits=10, decimal_places=2)
    price_discounted = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10)
    affiliate_link = models.URLField()
    image_urls = models.JSONField(default=list)  # Stores a list of image URLs
    rating = models.FloatField(blank=True, null=True)
    review_count = models.IntegerField(blank=True, null=True)
    stock_status = models.BooleanField(default=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    delivery_time = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
