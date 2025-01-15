from django.db import models
from django.contrib.auth import get_user_model
from worlds.models import Brand
User = get_user_model()

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

class MonthlyAllocation(models.Model):
  member = models.ForeignKey(Members, on_delete=models.CASCADE)
  month = models.DateField()
  tokenAllocation = models.FloatField(default=0.0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
      return f"{self.member.name}: {self.month}"