from rest_framework import serializers;
from .models import Score, Tokens

class ScoreSerializer(serializers.ModelSerializer):
  user = serializers.CharField(source='user.name', read_only=True)

  class Meta:
    model = Score
    fields = ['score', 'game', 'user', 'tokens']
    

class TokensSerializer(serializers.ModelSerializer):
  user = serializers.CharField(source='user.name', read_only=True)

  class Meta:
    model = Tokens
    fields = ['total_tokens', 'claimed_tokens', 'user']