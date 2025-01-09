from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class TokenInfo(models.Model):
  token_name = models.CharField(max_length=100)
  token_symbol = models.CharField(max_length=100, null=True, blank=True)
  solana_contract_address = models.CharField(max_length=700, null=True)
  bnb_contract_address = models.CharField(max_length=700, null=True, blank=True)
  total_value = models.FloatField(default=0, null=True, blank=True)
  total_tokens = models.FloatField(default=0, null=True, blank=True)
  token_prices = models.FloatField(default=0, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.token_name}"
  
  
class TokenPeriod(models.Model):
  tokenInfo = models.ForeignKey(TokenInfo, on_delete=models.CASCADE, null=True)
  token_count_date = models.DateField(null=True, blank=True)
  token_duration = models.IntegerField(default=0, null=True, blank=True)

class Game(models.Model):
  name = models.CharField(max_length=100)
  tokenInfo = models.ForeignKey('TokenInfo', on_delete=models.CASCADE, null=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)
  def __str__(self):
    return f"{self.name}"

class Brand(models.Model):
  name = models.CharField(max_length=100)
  tokenInfo = models.ManyToManyField(TokenInfo, blank=True)
  started_date = models.DateField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.name}"

class Members(models.Model):
  ROLE_CHOICES = [
    ('super_founder', 'Super Founder'),
    ('super_builder', 'Super Builder'),
    ('founder', 'Founder'),
    ('builder', 'Builder'),
    ('communicator', 'Communicator'),
    ('tourist', 'Tourist'),
    ('listener', 'Listener'),
  ]
  name = models.CharField(max_length=100)
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
  brands = models.ManyToManyField(Brand, blank=True)
  role = models.CharField(max_length=50, choices=ROLE_CHOICES)
  joined_date = models.DateField(null=True, blank=True)
  earned_tokens = models.FloatField(default=0.0, null=True, blank=True)
  earned_dollars = models.FloatField(default=0.0, null=True, blank=True)
  ownership = models.FloatField(default=0.0, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
      return f"{self.name}: {self.role}"

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

class MerkelDatastructure(models.Model):
  serialized_leaves = models.CharField(max_length=1000)
  modified_date = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


