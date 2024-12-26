from rest_framework import serializers;
from .models import Score, TokenInfo
class ScoreSerializer(serializers.ModelSerializer):
  user = serializers.CharField(source='user.name', read_only=True)
  game = serializers.CharField(source='game.name', read_only=True)
  class Meta:
    model = Score
    fields = ['score', 'game', 'user', 'tokens', 'claimed_tokens', 'last_claimed_date']
    

class TokenInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = TokenInfo
    fields = '__all__'