from rest_framework import serializers
from .models import Ad
from .models import World


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class WorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = World
        fields = ['id', 'name', 'ad_categories', 'created_at', 'updated_at']