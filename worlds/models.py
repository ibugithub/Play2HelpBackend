from django.db import models
from tokens.models import TokenInfo


class World(models.Model):
  name = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.name}"

class Brand(models.Model):
  name = models.CharField(max_length=100)
  world = models.ForeignKey(World, on_delete=models.CASCADE, null=True, blank=True)
  tokenInfo = models.ManyToManyField(TokenInfo, blank=True)
  started_date = models.DateField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.name}"
