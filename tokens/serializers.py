from rest_framework import serializers;
from .models import TokenInfo, MerkelDatastructure


class TokenInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = TokenInfo
    fields = '__all__' 
      
class MerkelDatastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerkelDatastructure
        fields = ['id', 'serialized_leaves', 'modified_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        