from django.db import models

# Create your models here.
class TokenInfo(models.Model):
  token_name = models.CharField(max_length=100)
  token_symbol = models.CharField(max_length=100, null=True, blank=True)
  solana_contract_address = models.CharField(max_length=700, null=True, blank=True)
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

class MerkelDatastructure(models.Model):
  serialized_leaves = models.CharField(max_length=1000)
  modified_date = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
