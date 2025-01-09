from django.urls import path
from .views import SubmitScoreView, ScoreListView, ListAllScores, GetScoreDataView, GetTotalScoresView, SetClaimTokensView, GetAllScoresWithTokenInfo

urlpatterns = [
  path('submitScore/', SubmitScoreView.as_view(), name='submit-score'),
  path('getScores/', ScoreListView.as_view(), name='score-list'),
  path('getAllScores/', ListAllScores.as_view(), name='all-scores'),
  path('setClaimTokens/', SetClaimTokensView.as_view(), name='claim_tokens'),
  path('getScoreData/', GetScoreDataView.as_view(), name='score_data'),
  path('getTotalScores/', GetTotalScoresView.as_view(), name='total_scores'),
  path('getAllScoresWithTokenInfo/', GetAllScoresWithTokenInfo.as_view(), name='all-scores')
]