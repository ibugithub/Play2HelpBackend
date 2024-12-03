from rest_framework import serializers;
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
  user = serializers.CharField(source='user.name', read_only=True)

  class Meta:
    model = Score
    fields = ['score', 'game', 'user', 'reward']