from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Score(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  game = models.CharField(max_length=100, unique=True)
  score = models.IntegerField()
  reward = models.FloatField(default=0.0)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.name}: {self.score}"