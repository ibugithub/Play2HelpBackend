from django.urls import path
from .views import SubmitScoreView, ScoreListView

urlpatterns = [
  path('submitScore/', SubmitScoreView.as_view(), name='submit-score'),
  path('getScores/', ScoreListView.as_view(), name='score-list')
]