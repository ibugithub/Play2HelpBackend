from django.urls import path
from .views import  getMemberData, CalculateOwnership

urlpatterns = [
  path('getMemberData/', getMemberData.as_view(), name='member_data'),
  path('calculateOwnership/', CalculateOwnership.as_view(), name='calculateOwnership'),
]