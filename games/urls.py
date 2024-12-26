from django.urls import path
from .views import SubmitScoreView, ScoreListView, ListAllScores, MerkelDataView, GetScoreDataView

urlpatterns = [
  path('submitScore/', SubmitScoreView.as_view(), name='submit-score'),
  path('getScores/', ScoreListView.as_view(), name='score-list'),
  path('getAllScores/', ListAllScores.as_view(), name='all-scores'),
  # path('setClaimTokens/', SetClaimTokensView.as_view(), name='claim_tokens'),
  path('setMerkelDatastructure/', MerkelDataView.as_view(), name='merkel_datastructure'),
  path('getScoreData/', GetScoreDataView.as_view(), name='score_data')
]