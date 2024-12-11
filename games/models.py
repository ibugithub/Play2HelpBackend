from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model

User = get_user_model()

class Score(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  game = models.CharField(max_length=100)
  score = models.IntegerField()
  tokens = models.FloatField(default=0.0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.user.name}: {self.score}"

class Tokens(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  total_tokens = models.FloatField(default=0.0)
  claimed_tokens = models.FloatField(default=0.0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
def __str__(self):
  return f"{self.user.name}: {self.total_tokens}"

