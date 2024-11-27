from django.urls import path
from .views import SubmitScoreView

urlpatterns = [
  path('submitScore/', SubmitScoreView.as_view(), name='submit-score')
]