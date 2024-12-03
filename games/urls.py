from django.urls import path
from .views import SubmitScoreView, ScoreListView, ListAllScores

urlpatterns = [
  path('submitScore/', SubmitScoreView.as_view(), name='submit-score'),
  path('getScores/', ScoreListView.as_view(), name='score-list'),
  path('getAllScores/', ListAllScores.as_view(), name='all-scores'),
]