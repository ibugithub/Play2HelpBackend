from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.utils import timezone 
from tokens.models import TokenInfo

User = get_user_model()

class Game(models.Model):
  name = models.CharField(max_length=100)
  tokenInfo = models.ForeignKey(TokenInfo, on_delete=models.CASCADE, null=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)
  def __str__(self):
    return f"{self.name}"

class Score(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  score = models.IntegerField()
  tokens = models.FloatField(default=0.0)
  claimed_tokens = models.FloatField(default=0.0)
  last_claimed_date = models.DateTimeField(default=timezone.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f"{self.user.name}: {self.score}"

class TotalScore(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  total_score = models.IntegerField()
  total_tokens = models.FloatField(default=0.0)
  claimed_tokens = models.FloatField(default=0.0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f"{self.user.name}: {self.total_score}"

