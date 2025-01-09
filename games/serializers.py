from rest_framework import serializers;
from .models import Score,TotalScore

class ScoreSerializer(serializers.ModelSerializer):
  user = serializers.CharField(source='user.name', read_only=True)
  game = serializers.CharField(source='game.name', read_only=True)
  class Meta:
    model = Score
    fields = ['score', 'game', 'user', 'tokens', 'claimed_tokens', 'last_claimed_date']
     
class TotalScoreSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = TotalScore
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.name
